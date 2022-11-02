/** @odoo-module **/
/* Copyright 2022 Solvve, Inc. <sales@solvve.com>
*  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl) */

import {SubscribeMenu} from '@web_push_base/js/subscribe_systray'
import {createComponent, dom, nextTick} from 'web.test_utils'
import {registry} from "@web/core/registry";
import {rpcService} from '@web/core/network/rpc_service'
import {ormService} from '@web/core/orm_service'
import {uiService} from '@web/core/ui/ui_service'
import {notificationService} from '@web/core/notifications/notification_service'
import {makeTestEnv} from "@web/../tests/helpers/mock_env";

const serviceRegistry = registry.category('services')

QUnit.module('WebPush', {
    async beforeEach() {
        serviceRegistry
            .add('rpc', rpcService)
            .add('orm', ormService)
            .add('ui', uiService)
            .add('notification', notificationService)
        /**@type{SubscribeMenu}*/
        this.subscribeMenu = await createComponent(SubscribeMenu, {
            env: await makeTestEnv(),
        })
    },
}, function () {
    QUnit.module('SubscribeMenu')

    QUnit.test('View', async function (assert) {
        assert.expect(1)
        const btnClass = '.wp-subscribe-systray__button'

        assert.containsOnce(this.subscribeMenu, btnClass)

        if (this.subscribeMenu.serviceWorkerAvailable) {
            const permissions = window.Notification.permission
            if (permissions === 'granted') {
                await dom.click(this.subscribeMenu.el.querySelector(btnClass))
                await nextTick()

                this.subscribeMenu.state.subscribeSwitch = true
                await this.subscribeMenu.save()

                await nextTick()

                this.subscribeMenu.state.subscribeSwitch = false
                await this.subscribeMenu.save()

                await dom.click(document.querySelector('.modal-dialog .close'))
                await nextTick()
            }
        }
    })

    if ('serviceWorker' in window.navigator) {
        QUnit.test('checkSubscription', async function (assert) {
            assert.expect(1)
            assert.ok(typeof await this.subscribeMenu.checkSubscription() === 'boolean')
        })

        QUnit.test('subscribe', async function (assert) {
            assert.expect(1)
            assert.ok(await this.subscribeMenu.subscribe() instanceof PushSubscription)
        })

        QUnit.test('unsubscribe', async function (assert) {
            assert.expect(1)
            assert.ok(typeof await this.subscribeMenu.unsubscribe() === 'boolean')
        })

        QUnit.test('updateDialogState', async function (assert) {
            assert.expect(1)
            assert.ok(await this.subscribeMenu.updateDialogState())
        })

        QUnit.test('save', async function (assert) {
            assert.expect(1)
            assert.ok(await this.subscribeMenu.save())
        })
    }

})