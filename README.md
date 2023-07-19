# postman-to-hurl
A small utility to simplify the process of moving away from postman. Barely tested, no refunds.

### Usage:
0. Install hurl. `apt-get install hurl` or `brew install hurl` etc.
1. Download your postman env from postman
2. Convert to a .env file with `postman-env-to-dot-env.py file.json > .env`
3. Download your schema from postman in V2 format
4. Convert the postman schema to hurl with `postman-to-hurl.py file.json > output.hurl` 
5. Import env `source .env`
6. Run hurl `cat output.hurl | hurl`

### Features:
1. Hurl is great


### Limitations:
1. No scripts. These will be added to your hurl script but commented out.
2. No schema validations. Again these will be added to the script but commented out.
3. No UI (possibly a feature)
