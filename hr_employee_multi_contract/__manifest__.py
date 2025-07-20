{
    'name': 'HR Employee Multi Contract',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Allow employees to have multiple active contracts simultaneously',
    'description': """
        This module disables the contract overlap validation that prevents employees 
        from having multiple active contracts at the same time.
        
        Features:
        - Disables the _check_current_contract constraint
        - Allows employees to have multiple contracts in 'open' or 'close' state
        - Maintains all other contract functionality
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['hr_contract'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
} 