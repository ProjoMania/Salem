/** @odoo-module **/

import { registry } from "@web/core/registry";
import { createElement, append } from "@web/core/utils/xml";
import { Notebook } from "@web/core/notebook/notebook";
import { formView } from "@web/views/form/form_view";
import { FormCompiler } from "@web/views/form/form_compiler";
import { FormRenderer } from "@web/views/form/form_renderer";
import { FormController } from '@web/views/form/form_controller';
import { useService } from "@web/core/utils/hooks";

export class VisitFormRenderer extends FormController {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
    }
    async onClickGpsLocation(e) {
        this.coords = {};
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                ({ coords: { latitude, longitude } }) => {
                    Object.assign(this.coords, {
                        latitude,
                        longitude,
                    });
                    this.rpc(
                        `/visit/save_location`,{
                        cords:this.coords,
                        id:this.model.root.resId

                        }
                    )
                    .then(function(){
                    location.reload()
                    })
                }
            );
        }
    }
}

export const VisitView = {
    ...formView,
    Controller: VisitFormRenderer,
};

registry.category("views").add("visit_form", VisitView);
