set -x

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots

python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots

sleep 3

python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots

python -m simplelab.dispatcher --type set --res slots --val 3

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots

sleep 3

python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"

python -m simplelab.dispatcher --type set --res slots --val 1

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots

sleep 3

python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"
python -m simplelab.dispatcher --type cmd --cmd "sleep 2 && echo ciao"

python -m simplelab.dispatcher --type get --res processes
python -m simplelab.dispatcher --type get --res queued
python -m simplelab.dispatcher --type get --res slots