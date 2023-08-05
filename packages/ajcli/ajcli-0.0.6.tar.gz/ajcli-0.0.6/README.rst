=======
ajcli
=======

example usage::

    $ jiracli --host "$JIRA_SERVER" -u "$USER" -p "$PASSWORD" worklog project="$KEY" sprint=2
    $ jiracli --host "$JIRA_SERVER" -u "$USER" issues --field 'key' -f 'summary' project="$KEY" sprint=2 type=issue
