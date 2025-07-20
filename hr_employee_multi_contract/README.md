# HR Employee Multi Contract

## Overview

This module disables the contract overlap validation in Odoo's HR Contract module, allowing employees to have multiple active contracts simultaneously.

## Problem

By default, Odoo's HR Contract module includes a constraint (`_check_current_contract`) that prevents employees from having multiple contracts in 'open' or 'close' state at the same time. This constraint raises a ValidationError when trying to create overlapping contracts.

## Solution

This module overrides the `_check_current_contract` method to do nothing, effectively disabling the constraint while maintaining all other contract functionality.

## Features

- **Disabled Overlap Validation**: Employees can now have multiple active contracts
- **Preserved Functionality**: All other contract features remain intact
- **Simple Implementation**: Clean override without complex logic

## Installation

1. Install the module through Odoo's Apps menu
2. The constraint will be automatically disabled
3. No additional configuration required

## Usage

After installation, you can:
- Create multiple contracts for the same employee
- Have contracts with overlapping date ranges
- Maintain contracts in 'open' or 'close' state simultaneously

## Technical Details

The module inherits from `hr.contract` and overrides the `_check_current_contract` method:

```python
def _check_current_contract(self):
    """
    Override the original method to disable contract overlap validation.
    This allows employees to have multiple active contracts simultaneously.
    """
    # Do nothing - this disables the constraint
    pass
```

## Dependencies

- `hr_contract` (Odoo core module)

## License

LGPL-3 