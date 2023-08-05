=======
ajcli
=======

example usage::

    $ jiracli --host "$JIRA_SERVER" -u "$USER" -p "$PASSWORD" projects
    $ jiracli --host "$JIRA_SERVER" -p "$PASSWORD" worklogs project="$KEY" and sprint=2
    $ jiracli --host "$JIRA_SERVER" -u "$USER" worklogs --user "Foo Bar" sprint=2 or sprint=3
    $ jiracli --host "$JIRA_SERVER" issues project="$KEY" and type=story or type=issue
    $ jiracli --host "$JIRA_SERVER" users "$PROJECT_ID"
