# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route


class PWA(Controller):
    '''
    PWA supports
    '''
    def get_asset_urls(self, asset_xml_id):
        '''
        get the asset urls
        :param asset_xml_id:
        :return:
        '''
        qweb = request.env["ir.qweb"].sudo()
        assets = qweb._get_asset_nodes(asset_xml_id)
        urls = []
        for asset in assets:
            if asset[0] == "link":
                urls.append(asset[1]["href"])
            if asset[0] == "script":
                urls.append(asset[1]["src"])
        return urls

    @route("/anita-service-worker.js", type="http", auth="public")
    def service_worker(self):
        '''
        service worker
        :return:
        '''
        qweb = request.env["ir.qweb"].sudo()
        urls = []
        urls.extend(self.get_asset_urls("web.assets_common"))
        urls.extend(self.get_asset_urls("web.assets_backend"))
        version_list = []
        for url in urls:
            version_list.append(url.split("/")[3])
        cache_version = "-".join(version_list)
        mimetype = "text/javascript;charset=utf-8"
        content = qweb._render(
            "anita_pwa.service_worker", {
                "anita_pwa_cache_name": cache_version,
                "anita_pwa_files_to_cache": urls
            },
        )
        return request.make_response(content, [("Content-Type", mimetype)])

    @route("/anita_pwa/manifest", type="http", auth="public")
    def manifest(self):
        '''
        :return: return the manifest
        '''
        qweb = request.env["ir.qweb"].sudo()

        pwa_config = request.env["res.config.settings"].get_anita_pwa_config()
        pwa_name = pwa_config["pwa_name"] or 'Funenc'
        pwa_short_name = pwa_config["pwa_short_name"] or 'Funenc'

        icon128x128 = pwa_config.get("pwa_icon_128", False)
        icon144x144 = pwa_config.get("pwa_icon_144", False)
        icon152x152 = pwa_config.get("pwa_icon_152", False)
        icon192x192 = pwa_config.get("pwa_icon_192", False)
        icon256x256 = pwa_config.get("pwa_icon_256", False)
        icon512x512 = pwa_config.get("pwa_icon_512", False)

        pwa_background_color = pwa_config["pwa_background_color"]
        pwa_theme_color = pwa_config["pwa_theme_color"]

        mimetype = "application/json;charset=utf-8"

        content = qweb._render("anita_pwa.manifest", {
            "pwa_name": pwa_name,
            "pwa_short_name": pwa_short_name,
            "icon128x128": icon128x128,
            "icon144x144": icon144x144,
            "icon152x152": icon152x152,
            "icon192x192": icon192x192,
            "icon256x256": icon256x256,
            "icon512x512": icon512x512,
            "start_url": "/web",
            "pwa_background_color": pwa_background_color,
            "pwa_theme_color": pwa_theme_color,
        })

        return request.make_response(content, [("Content-Type", mimetype)])
