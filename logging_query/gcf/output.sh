
#!/bin/bash
Var1="e2e_delay"
Var2="response_time"


if [ $2 = "$Var1" ]
then    
    python3.9 transform_google_logging.py -g $1 -l $2 -d $1 -m $3
elif [ $2 = "response_time" ]
then
    python3.9 transform_google_logging.py -g $1 -m $3
fi