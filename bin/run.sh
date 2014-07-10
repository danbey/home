#!/bin/bash

echo "Pid is $$"
echo -n "Press Enter.." 
read 
exec $@
