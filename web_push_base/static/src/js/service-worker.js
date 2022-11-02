/* Copyright 2022 Solvve, Inc. <sales@solvve.com>
*  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl) */

/**
 * @typedef {ServiceWorkerGlobalScope} self
 */

self.addEventListener('push', function (event) {
    const pushData = event.data.json()
    const notificationOptions = {
        body: pushData.body || undefined,
        icon: pushData.icon || undefined,
        data: pushData.data || undefined,
        actions: pushData.actions || undefined,
        image: pushData.image || undefined,
        requireInteraction: true,
    }
    event.waitUntil(
        self.registration.showNotification(pushData.title, notificationOptions)
    );
});

self.addEventListener('notificationclick', function (event) {
    const {data} = event.notification
    const url = data[event.action]
    if (url) {
        self.clients.openWindow(url).then();
    } else if (data.defaultURL) {
        self.clients.openWindow(data.defaultURL).then();
    }
}, false);
