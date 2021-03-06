README - Monitor Report Generator


Requirements: Python 2.7


Input file structure: received_time sent_time sent_from action subject

        e.g. 1508405807340 1508405807350 luke HELLO
             1508405807378 1508405807387 luke LOST vader
             1508405807467 1508405807479 luke FOUND r2d2

        - received_time and sent_time are integers
        - sent_from, action and subject are string
        - action can only be either HELLO, FOUND or LOST
        - action FOUND and LOST require subject
        - whitespace can be at the beginning or end of the notification
          but only allow one whitespace in between the content


Run: python monitor_report_generator input.txt


Notice: - Please place the text file in the same folder
        - Must specify the input file
        - Allow more arguments, e.g. foo bar, but will be ignored as this
          do not mean anything


Unit Test: python -m unittest test_notification

Assumption: - UNKNOWN is when there are more than one notifications within 50ms timestamp
              and there exist a notification prove node X is DEAD whereas another prove X is still ALIVE.
              (do not know which is the most recent update --> UNKONWN)
            - If a node is UNKNOWN, the report will also list all notification that causing this.
              e.g. luke UNKNOWN 1508405807467 vader LOST luke, 1508405807457 luke FOUND r2d2
