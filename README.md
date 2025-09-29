# fido-activity-parse

Parses fidelity activity files

To run:

```
rm ~/Downloads/Accounts_history.csv
# download activity from fidelity
uv run src/fido-activity-parse.py  --account "Trust Brokerage" --account "Joint Checking" < ~/Downloads/Accounts_History.csv
```

