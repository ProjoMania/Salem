/** @odoo-module **/
import { Component, useState, useEffect } from "@odoo/owl";
import { AccountReport } from "@account_reports/components/account_report/account_report";


class ReportCurrencyDropdown extends Component {
    static template = "aged_receivable_currency.CurrencyDropdownTemplate";
}

AccountReport.components = {
    ...AccountReport.components,
    CurrencyDropdown: ReportCurrencyDropdown,
}

    // setup() {
    //     this.state = useState({
    //         activeCurrencies: [],
    //         selectedCurrency: this.props.selectedCurrency,
    //     });

    //     this.orm = useService("orm");

    //     console.log("Setup CurrencyDropdown");

    //     // onWillStart(async () => {
    //     //     // Set activeCurrencies
    //     //     console.log("Set activeCurrencies");
    //     //     const currencies = await this.orm.searchRead("res.currency", [], ["name"]);
    //     //     console.log(currencies);
    //     //     this.setState({ activeCurrencies: currencies });
    //     // });

    //     this.logActiveCurrencies();
    // }

    // logActiveCurrencies() {
    //     console.log(this.state.activeCurrencies);
    // }



// export class AccountCurrencyBar extends AccountReportButtonsBar {}

// AccountCurrencyBar.components = {
//     ...AccountReportButtonsBar.components,
//     CurrencyDropdown: ReportCurrencyDropdown,
// }