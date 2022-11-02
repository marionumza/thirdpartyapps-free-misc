/** @odoo-module **/
/* Copyright 2022 Solvve, Inc. <sales@solvve.com>
*  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl) */

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
 *     remove: Boolean,
 * }} SubscribeMenuItemState
 */


/**
 * @property {SubscribeMenuItemState} state
 */
export class SubscribeMenuItem extends Component {
    setup() {
        super.setup();
        this.state = useState({
            remove: false,
        })
    }

    tiggerUpdateState() {
        this.trigger('updateState', {
            remove: this.state.remove,
            hash: this.props.subscription.hash,
        })
    }

    markToRemove() {
        this.state.remove = true
        this.tiggerUpdateState()
    }

    unMarkToRemove() {
        this.state.remove = false
        this.tiggerUpdateState()
    }
}

Object.assign(SubscribeMenuItem, {
    template: 'web_push_base.SubscribeMenuItem',
})
