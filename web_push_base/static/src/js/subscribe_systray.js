/** @odoo-module **/
/* Copyright 2022 Solvve, Inc. <sales@solvve.com>
*  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl) */

import {registry} from '@web/core/registry'
import {useService} from '@web/core/utils/hooks'
import OwlDialog from 'web.OwlDialog'
import {_t} from 'web.core'
import {SubscribeMenuItem} from '@web_push_base/js/subscription_item'

const {Component, useState} = owl


/**
 * @typedef {{
 *     name: String,
 *     hash: String,
 *     create_date: String,
 * }} SubscriberItem
 */

/**
 * @typedef {{
 *     subscribed: Boolean,
 *     subscribeSwitch: Boolean,
 *     open: Boolean,
 *     subscriberItems: SubscriberItem[],
 *     status: 'idle'|'pending',
 *     subscribers2Remove: String[],
 *     targetHash: String,
 * }} SubscribeMenuState
 */

/**
 * @typedef {{
 *     subscribed: Boolean,
 *     targetHash: String,
 *     subscriberItems: SubscriberItem[],
 * }} SubscriberSystrayData
 */

/**
 * @property {SubscribeMenuState} state
 * @property {ServiceWorkerRegistration|undefined} sw
 */
export class SubscribeMenu extends Component {
    setup() {
        super.setup()
        this.orm = useService('orm')
        this.notification = useService('notification')
        this.subscripsionDOMId = _.uniqueId('subscription-state-')
        this.state = useState({
            subscribed: false,
            subscribeSwitch: false,
            open: false,
            subscriberItems: [],
            subscribers2Remove: [],
            status: 'idle',
            targetHash: '',
        })
        this.sw = undefined
    }

    async willStart() {
        await super.willStart(...arguments);
        [this.sw] = await navigator.serviceWorker.getRegistrations();
    }

    mounted() {
        super.mounted(...arguments)
        if (this.serviceWorkerAvailable) {
            this.checkSubscription().then(subscribed => {
                this.state.subscribed = subscribed
                this.state.subscribeSwitch = subscribed
            })
        } else {
            console.error('ServiceWorker is not supported')
            this.notification.add(_t('ServiceWorker is not supported'), {type: 'danger'})
            this.destroy();
            return null;
        }
    }

    /**
     * @returns {Boolean}
     */
    get serviceWorkerAvailable() {
        return 'serviceWorker' in window.navigator
    }

    /**
     * @returns {Boolean}
     */
    get hasSubscribers() {
        return Boolean(this.state.subscriberItems.length)
    }

    /**
     * @returns {String}
     */
    get dialogSize() {
        return this.hasSubscribers ? 'medium' : 'small'
    }

    get dialogTitle() {
        return _t('Web Push Settings')
    }

    get isPending() {
        return this.state.status === 'pending'
    }

    /**
     * @param {PushSubscription} subscription
     * @returns {Promise<SubscriberSystrayData>}
     * @private
     */
    async _loadSystrayData(subscription) {
        return await this.rpc('/web_push/systray', {
            subscription: subscription ? subscription.toJSON() : '',
        })
    }

    /**
     * @returns {Promise<Boolean>}
     */
    async checkSubscription() {
        if (!this.sw) {
            return false
        }
        const subscription = await this.sw.pushManager.getSubscription()
        if (!subscription) {
            return false
        }
        return await this.orm.call('web_push.subscriber', 'is_subscriber_available', [subscription.toJSON()])
    }

    /**
     * @returns {Promise<PushSubscription>}
     */
    async subscribe() {
        this.sw = await navigator.serviceWorker.register('/web_push_base/static/src/js/service-worker.js')
        let subscription = await this.sw.pushManager.getSubscription()

        if (subscription && this.state.subscribed) {
            return subscription
        } else if (subscription) {
            await subscription.unsubscribe()
        }

        const vapidPublicKey = new Uint8Array(await this.rpc('/web_push/public_key/uint8_array'))

        subscription = await this.sw.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: vapidPublicKey,
        })

        await this.rpc('/web_push/subscribe', {subscription})

        return subscription
    }

    /**
     * @returns {Promise<Boolean>}
     */
    async unsubscribe() {
        if (!this.sw) {
            return false
        }
        const subscription = await this.sw.pushManager.getSubscription()
        if (subscription) {
            await subscription.unsubscribe()
            await this.rpc('/web_push/unsubscribe', {subscription})
            return true
        }
        return false
    }

    /**
     * Close Settings Dialog
     */
    async closeDialog() {
        this.state.subscriberItems = []
        this.state.open = false
        this.checkSubscription().then((subscribed) => {
            this.state.subscribed = subscribed
        })
        return true
    }

    /**
     * Open Settings Dialog
     * @returns {Promise<boolean>}
     */
    async openDialog() {
        await this.updateDialogState()
        this.state.open = true
    }

    /**
     * @returns {Promise<Boolean>}
     */
    async updateDialogState() {
        if (!this.sw) {
            return false
        }
        const subscription = await this.sw.pushManager.getSubscription()
        const {subscriberItems, subscribed, targetHash} = await this._loadSystrayData(subscription)
        Object.assign(this.state, {
            subscriberItems: subscriberItems,
            subscribed: subscribed,
            subscribeSwitch: subscribed,
            targetHash: targetHash,
        })
        return true
    }

    /**
     * @returns {Promise<Boolean>}
     */
    async save() {
        if (this.state.subscribeSwitch) {
            /**@type{NotificationPermission}*/
            let permission = Notification.permission

            if (permission !== 'granted') {
                permission = await Notification.requestPermission()
            }

            if (permission === 'granted') {
                await this.subscribe()
            } else {
                throw Error()
            }
        } else {
            await this.unsubscribe()
        }

        const {subscribers2Remove} = this.state

        if (subscribers2Remove.length) {
            await this.rpc('/web_push/unlink_by_hash', {hash_items: subscribers2Remove})
        }

        this.notification.add(_t('Saved'), {type: 'success'})

        return true
    }

    /**
     * @param {{
     *     remove: Boolean,
     *     hash: String,
     * }} item
     */
    onUpdateSubscriptionState({detail: item}) {
        const removeIndex = this.state.subscribers2Remove.indexOf(item.hash)
        const append = item.remove && removeIndex === -1
        if (append) {
            this.state.subscribers2Remove.push(item.hash)
        } else if (!append) {
            this.state.subscribers2Remove.splice(removeIndex, 1)
        }
    }

    async onDiscard() {
        await this.closeDialog()
        this.state.status = 'idle'
    }

    async onSave() {
        this.state.status = 'pending'
        try {
            await this.save()
            await this.closeDialog()
        } catch (e) {
            console.error(e)
        } finally {
            this.state.status = 'idle'
        }
    }
}

Object.assign(SubscribeMenu, {
    template: 'web_push_base.SubscribeMenu',
    components: {Dialog: OwlDialog, SubscribeMenuItem},
})

registry.category('systray').add('SubscribeMenu', {
    Component: SubscribeMenu,
    isDisplayed() {
        return 'serviceWorker' in window.navigator
    }
}, {
    sequence: 12,
})