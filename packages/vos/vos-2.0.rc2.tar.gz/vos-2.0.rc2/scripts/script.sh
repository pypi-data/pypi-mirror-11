#!/bin/tcsh
#
#$ -S /bin/tcsh
#$ -j y

python2.6 mountvofs --readonly --cache_nodes --cache_limit=500000 --vospace=vos:durand --mountpoint=/ephemeral/vospace --cache_dir=/ephemeral/vos_cache --max_flush_threads=5 --allow_other

setenv vodirectory  "/ephemeral/vospace"
echo "hst_cache_process: Starting "
date
echo 'hst_cache_process: ------------Starting the execution Version 3---------------------'

echo 'hst_cache_process: ------------Who am I----------------------------------'
whoami
echo $USER

echo 'hst_cache_process: ------------print_env--------------------------'
printenv


date
echo 'hst_cache_process: ------------Setting environment--------------------------'
setenv HOME ${HOME}
setenv home ${HOME}

date
echo 'hst_cache_process: ------------My ip--------------------------'
/sbin/ifconfig | grep 192

if ! (-d /ephemeral/vospace/crds)  then
   echo 'hst_cache_process: Sleeping 120 for the VOSPACE cause'
   sleep 120
endif 

date
if (-d /ephemeral/vospace/crds)  then
   echo 'hst_cache_process: /ephemeral/vospace is a mountpoint'
else
   echo 'hst_cache_process: /ephemeral/vospace is not mountpoint sleeping again 60 '
   sleep 60
endif

date
if (-d /ephemeral/vospace/crds)  then
   echo 'hst_cache_process: /ephemeral/vospace is a mountpoint'
else
   echo 'hst_cache_process: /ephemeral/vospace is not mountpoint sleeping again 240 sec in case'
   sleep 240
endif

date
if(-d /ephemeral/vospace/crds)  then
   echo 'hst_cache_process: /ephemeral/vospace is a mountpoint'
else
   echo 'hst_cache_process: giving up, exiting, sorry. Dumping vos.err and mount log'
   cat /tmp/vos.err
   exit -1
endif

echo 'Looking at VOSPACE existence with cat /etc/mtab '
cat /etc/mtab

date
echo 'hst_cache_process: Looking at VOSPACE existence with ls '
\ls /ephemeral/vospace/crds
mkdir /ephemeral/hubble
mkdir /ephemeral/hubble/otfr

echo 'hst_cache_process: arguments'
echo "hst_cache_process: Hostname         = " `hostname`
echo "hst_cache_process: CacheSoftwareDir = " $1
echo "hst_cache_process: Dataset          = " $2
echo "hst_cache_process: Step             = " $3
echo ""

echo "hst_cache_process: Change to the CONDOR-defined working directory"

if ($?TMPDIR) then
   cd $TMPDIR
   echo "hst_cache_process: TMPDIR           = " $TMPDIR
else
  echo "hst_cache_process: No TMPDIR specified"
endif

echo "hst_cache_process: executing in the following directory: "
pwd

date
echo 'hst_cache_process: Looking at VOSPACE existence with cat /etc/mtab'
cat /etc/mtab

echo 'hst_cache_process: Looking at VOSPACE existence with ls'
\ls /ephemeral/vospace/crds

date
echo 'hst_cache_process: Checking the existence and status of server_config'
cat /ephemeral/vospace/crds/config/hst/server_config 
set v=$status
while ($v != 0)
echo 'Sleeping 5 seconds because server_config problem'
sleep 5
cat /ephemeral/vospace/crds/config/hst/server_config 
set v=$status
end


date
echo " "
date
echo "======================================================"
echo "Now the vofs log********************************************"
ls -lrt /tmp/vos.err
cat /tmp/vos.err
echo "End of vofs log*********************************************"

echo "======================================================"
echo "hst_cache_process: Processing returned with status: " $status
echo "hst_cache_process: Finished executing: " $2 $3
echo "hst_cache_process: Ending "
echo " "
echo " "
echo '------------Ending the execution---------------------'

date
