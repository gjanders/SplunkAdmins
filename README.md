## SplunkBase
Also available on SplunkBase as [Alerts for Splunk Admins](https://splunkbase.splunk.com/app/3796/)
For some searches you will need the companion app, the TA-Alerts for Splunk Admins app [TA-Alerts for SplunkAdmins github](https://github.com/gjanders/TA-SplunkAdmins/) or [TA-Alerts for SplunkAdmins splunkbase](https://splunkbase.splunk.com/app/6518/)

You may also be interested in [VersionControl For Splunk](https://splunkbase.splunk.com/app/4355/) or perhaps [Decrypt2](https://splunkbase.splunk.com/app/5565/)

## Introduction
This application accompanies the Splunk conf 2017 presentation "How did you get so big? Tips and tricks for growing your Splunk installation from 50GB/day to 1TB/day"

The overall idea behind this application is to provide a variety of alerts that detect issues or potential issues within the splunk log files and then advise via an alert that this has occurred
This application was built as there were a variety of messages in the Splunk console and logs in Splunk that if acted upon could have prevented an issue within the environment.

The original presentation is available as a [recording](http://conf.splunk.com/files/2017/recordings/howd-you-get-so-big-tips-n-tricks-for-growing-your-splunk-deployment-from-50-gb-per-day-to-1-tb-per-day.mp4) or [PDF](http://conf.splunk.com/files/2017/slides/howd-you-get-so-big-tips-tricks-for-growing-your-splunk-deployment-from-50-gb-day-to-1-tb-day.pdf)
The powerpoint should it be required is available [here](https://github.com/gjanders/splunkconf2017)

There are many potential alerts that might cause an issue so this application has all alerts disabled by default, post-installation once the required macros are configured you can enable the alerts you wish to use and add the required actions

There are also dashboards for investigating indexer performance, heavy forwarder queue usage, data model acceleration issues among other items that may be of interest to a Splunk admin

Please note that the all alerts & dashboards were tested on Linux-based Splunk infrastructure, with AIX, Linux and Windows forwarders

If you are running your Splunk enterprise installation on Windows or have customised your installation directory you will need to customise some of the macros such as `splunkadmins_splunkd_source` to point to the correct splunkd log file location

Also note that this application contains a very large number of alerts which you can use, you may wish to utilise the `allow_skew` in savedsearches.conf to allow the scheduler to balance out the scheduled alerts execution times

Finally, the application has evolved over the years, more recent releases have resulted in very generic alerts such as `AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only`, this is designed as a "catch all" to cover many splunkd log messages. The older alerts are very specific as the team I worked in was new to Splunk and required a more specific outcome/action based on each alert
Feel free to use either, and feedback or contributions via github or email are always welcome

## Macros - required configuration
The various saved searches and dashboards use macros within their searches, you will need to update the macros to ensure the searches/dashboards work as expected
To check the contents of the macros in Splunk 7 or newer, use CTRL-SHFT-E within the search window

The macros are listed below, many expect a `host=A OR host=B` item to assist in narrowing down a search while others expect only a single value...note that for `splunk_server` values they are always lower-case and case-sensitive!

`indexerhosts - a host=...` list of your indexers (for example `host=indexer1 OR host=indexer2`)

`heavyforwarderhosts - a host=...` list of your heavy forwarders (for example `host=heavyforwarder1 OR host=heavyforwarder2`)

`searchheadhosts - a host=...` list of your search head(s) (for example `host=searchhead1 OR host=searchhead2`)

`localsearchheadhosts - a host=...` list of your search head(s) within the cluster that these alerts are running on

`splunkenterprisehosts - a host=...` list of any Splunk enterprise instance (for example `host=indexer1 OR host=searchhead1 OR ...`)

`deploymentserverhosts - a host=...` list of deployment server(s) (for example `host=splunkdeploymentserver`)

`licensemasterhost - a host=...` entry for the license master server (for example `host=splunklicensemaster`)

`searchheadsplunkservers - a splunk_server=...` list of any Splunk search head hosts (for example `splunk_server=searchhead*`)

`splunkindexerhostsvalue - a splunk_server=...` list of any Splunk indexer hosts (for example `splunk_server=indexer*`), or a `splunk_server_group=indexer_group`

`splunkadmins_splunkd_source` - this defaults to `source=*splunkd.log`, for a slight improvement in performance you can make this a specific file such as `/opt/splunk/var/log/splunk/splunkd.log`

`splunkadmins_splunkuf_source` - this defaults to `source=*splunkd.log`, you may wish to narrow down this location if your splunkd logs on universal forwarders have consistent installation directories

`splunkadmins_mongo_source` - this defaults to `source=*mongod.log`, for a slight improvement in performance you can make this a specific file such as `/opt/splunk/var/log/splunk/mongod.log`

`splunkadmins_clustermaster_oshost - a host=...` entry for the cluster master server (for example `host=splunkclustermaster`)

The macros are used in various alerts which you can optionally enable, the alerts will raise a triggered alert only as emails are not allowed for Splunk app certification purposes
The macros are also used in the dashboards for this application

There are also other macros you might want to consider editing before enabling the alerts, for example `splunkadmins_replicationfactor`.

The vast majority of the alerts also have a macro(s) which you can customise to tweak the search results, for example the macro `splunkadmins_weekly_truncated` allows the alert, `IndexerLevel - Weekly Truncated Logs Report`, to be customised without changing the alert itself. This will make upgrading to a new version of this app more straightforward
I have attempted to provide an appropriate macro in any alert where I deemed it appropriate, feedback is welcome for any alert that you believe should have a macro or requires further improvement

## Installation
The application is designed to work on a search head or search head cluster instance, installation on the indexing tier is not required. You may wish to use your monitoring console server as the search head to run this app on (as it will have `splunk_server_groups` configured for your environment).
There are a few searches that use REST API calls which are specific to the search head cluster they run on. These alerts will have to be placed on each search head or search head cluster, alternatively any server with the required search peers will also work, the relevant alerts are:
- `SearchHeadLevel - Accelerated DataModels with All Time Searching Enabled`
- `SearchHeadLevel - Realtime Scheduled Searches are in use`
- `SearchHeadLevel - Realtime Search Queries in dashboards`
- `SearchHeadLevel - Scheduled Searches without a configured earliest and latest time`
- `SearchHeadLevel - Scheduled searches not specifying an index`
- `SearchHeadLevel - Scheduled searches not specifying an index macro version`
- `SearchHeadLevel - Scheduled Searches Configured with incorrect sharing`
- `SearchHeadLevel - Saved Searches with privileged owners and excessive write perms`
- `SearchHeadLevel - User - Dashboards searching all indexes`
- `SearchHeadLevel - User - Dashboards searching all indexes macro version`
- `SearchHeadLevel - Users exceeding the disk quota (recent jobs list uses a REST call so you may need to adjust the search), the SearchHeadLevel - Users exceeding the disk quota introspection is a non-search head specific alternative`

The following reports also are specific to a search head or search head cluster:
- `SearchHeadLevel - Alerts that have not fired an action in X days`
- `SearchHeadLevel - Data Model Acceleration Completion Status`
- `SearchHeadLevel - Macro report`
- `What Access Do I Have?`

The following dashboards are search head or search head cluster specific:
- `Data Model Rebuild Monitor`
- `Data Model Status`

The following reports / alert must either run on the cluster master or a server where the cluster master is a peer:
- `ClusterMasterLevel - Per index status`
- `ClusterMasterLevel - Primary bucket count per peer`

## Dependencies
This application is designed to work independently of other Splunk applications, however there are a few reports and dashboards that rely on external apps to work as expected, these include:

Dashboards:
- `splunk_forwarder_data_balance_tuning` - the ScatterPlot visualization relies on the Splunk MLTK (Machine Learning Toolkit), note the dashboard works without this as well

Alerts/Reports:
- `IndexerLevel - RemoteSearches Indexes Stats Wilcard`
- `IndexerLevel - RemoteSearches Indexes Stats`
- `SearchHeadLevel - audit logs showing all time searches`
- `SearchHeadLevel - platform_stats access summary`
- `SearchHeadLevel - Script failures in the last day`
- `SearchHeadLevel - Search Queries summary exact match`
- `SearchHeadLevel - Search Queries summary non-exact match`
- `SearchHeadLevel - Searches dispatched as owner by other users`
- `SearchHeadLevel - Search Messages field extractor slow`
- `SearchHeadLevel - Search Messages user level`
- `SearchHeadLevel - Search Messages admins only`
- `SearchHeadLevel - SmartStore cache misses - dashboards`
- `SearchHeadLevel - SmartStore cache misses - savedsearches`
= `SearchHeadLevel - SmartStore cache misses - combined`

Will have more accurate search results with the base64 decoding working, [decrypt2 github](https://github.com/gjanders/decrypt2) or [decrypt2 SplunkBase](https://splunkbase.splunk.com/app/5565/) can work for this situation, you will need to update the macro `base64decode` in this app once decrypt2 is installed 

The following alerts/reports:
- `IndexerLevel - RemoteSearches Indexes Stats Wilcard`
- `SearchHeadLevel - Search Queries summary non-exact match`
- `SearchHeadLevel - Dashboards using depends and running searches in the background   `

Require the [TA-Alerts for SplunkAdmins github](https://github.com/gjanders/TA-SplunkAdmins/) or [TA-Alerts for SplunkAdmins splunkbase](https://splunkbase.splunk.com/app/6518/) to work as sexpected

## Using the application
Once the application is installed, **all** alerts are disabled by default and you can enable those you require or want to test in your local environment
If you choose not to customise the macros then many searches will search for all hosts, which will make the alerts and dashboards inaccurate!

## Which alerts should be enabled?
The alerts are all useful for detecting a variety of different scenarios which may or may not be applicable within your Splunk environment, in many ways this application has evolved into a library of possible alerts or explanation of alerts, it does not make sense to turn on all the alerts as such as some overlap

The description field has an (extremely) simple way of determining if an alert will require action, there are three levels:
  - Low - the alert is informational and likely relates to a potential issue, these alerts may produce false alarms
  - Moderate - the alert is a warning, most likely further action will need to be taken, a moderate chance of false alarms
  - High - the alert is likely relating to something that requires action and there is a very low chance that this will create false alarms

I do not have a nice way to auto-enable various alerts excluding editing the local/savedsearches.conf or via the GUI, any contribution of a setup file would be welcome here!

## How is this application used?
In the current environment the vast majority of the alerts are enabled to detect issues, they raise automated tickets or email depending on the urgency of the specific alert.
There are a few environment characteristics that may require changes to the way the app is used, and feedback is welcome if there is a nicer way to structure the alerts/application
The overall assumption is that the admin(s) are not carefully watching the splunkd logs or the messages in the console of the monitoring server/Splunk servers

## How is this application tested?
Before 2019 the universal forwarders in use are installed on a mix of Windows, Linux & AIX servers, in 2019 and beyond the testing scope has been vastly reduced to focus primarily on Splunk enterprise servers
All heavy forwarders, and Splunk enterprise installations are Linux based, while I expect the alerts will work with only changes to the macros.conf for a Windows based environment this remains untested
The test environment for this application has a single indexer cluster and two search head clusters

## Why was this application and associated conf talk created?
Inspired by articles such as "Things I wish I knew then" and knowledge collected from various conference replays, SplunkAnswers, 200+ support tickets & nearly four years of working on a Splunk environment I decided that I would attempt to share what I have learned in an attempt to prevent others from repeating the same mistakes
There are many Splunk conf talks available on this subject in various conference replays, however my goal was to provide practical steps to implement the ideas. That is why this application exists

## Which alerts are best suited to automation?
- `SearchHeadLevel - Scheduled searches not specifying an index`
- `SearchHeadLevel - Scheduled Searches Configured with incorrect sharing`
- `SearchHeadLevel - Splunk login attempts from users that do not have any LDAP roles`
- `SearchHeadLevel - Scheduled Searches That Cannot Run`
- `SearchHeadLevel - Scheduled Searches without a configured earliest and latest time`
- `SearchHeadLevel - Users exceeding the disk quota`
- `SearchHeadLevel - Users with auto-finalized searches`
- `SearchHeadLevel - User - Dashboards searching all indexes`
- `SearchHeadLevel - Detect Excessive Search Use - Dashboard - Automated`
- `SearchHeadLevel - WLM aborted searches`
- `SearchHeadLevel - Dashboards with all time searches set`
- `SearchHeadLevel - SavedSearches using special characters`
- `SearchHeadLevel - Dashboards using special characters`
- `SearchHeadLevel - Dashboards using depends and running searches in the background`
- `SearchHeadLevel - Summary searches using realtime search scheduling`
- `SearchHeadLevel - Searches dispatched as owner by other users`
- `SearchHeadLevel - Search Messages user level`
- `SearchHeadLevel - audit logs showing all time searches`

Are all well suited to an automated email using the sendresults command or a similar function as they involve end user configuration which the individual can change/fix

## Which alerts and reports have been tested on the newer Splunk versions such as 8.2 or 9.0?
This application was first created in 2017 and both Splunk and the application have evolved during this time period. This application is a library of potential alerts that could be used in a Splunk environment so it would never be a good idea to turn on all alerts from this application.

The below list of alerts and reports are actively used since version 8.0.x and in 8.2.x and eventually 9.0:
- `AllSplunkEnterpriseLevel - error in stdout.log`
- `AllSplunkEnterpriseLevel - Email Sending Failures`
- `AllSplunkEnterpriseLevel - Losing Contact With Master Node`
- `AllSplunkEnterpriseLevel - Replication Failures`
- `AllSplunkEnterpriseLevel - Splunk Scheduler skipped searches and the reason`
- `AllSplunkEnterpriseLevel - Splunkd Crash Logs Have Appeared in Production`
- `AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only`
- `AllSplunkLevel - Data Loss on shutdown`
- `AllSplunkLevel - TailReader Ignoring Path`
- `AllSplunkLevel - Time skew on Splunk Servers`
- `AllSplunkLevel - Unexpected termination of a Splunk process unix`
- `ClusterMasterLevel - excess buckets on master`
- `DeploymentServer - Error Found On Deployment Server`
- `ForwarderLevel - Channel churn issues`
- `ForwarderLevel - Data dropping duration`
- `ForwarderLevel - File Too Small to checkCRC occurring multiple times`
- `ForwarderLevel - Splunk HEC issues`
- `IndexerLevel - ClusterMaster Advising SearchOrRep Factor Not Met`
- `IndexerLevel - Data parsing error`
- `IndexerLevel - IndexConfig Warnings from Splunk indexers`
- `IndexerLevel - Indexer Queues May Have Issues`
- `IndexerLevel - Indexer replication queue issues to some peers`
- `IndexerLevel - Peer will not return results due to outdated generation`
- `IndexerLevel - platform_stats.counters hosts`
- `IndexerLevel - platform_stats.counters hosts 24hour`
- `IndexerLevel - platform_stats.indexers stddev measurement`
- `IndexerLevel - platform_stats.indexers stddev incoming measurement`
- `IndexerLevel - platform_stats.indexers totalgb measurement`
- `IndexerLevel - platform_stats.indexers totalgb_thruput measurement`
- `IndexerLevel - replicationdatareceiverthread close to 100% utilisation`
- `IndexerLevel - RemoteSearches find datamodel acceleration with wildcards`
- `IndexerLevel - RemoteSearches Indexes Stats`
- `IndexerLevel - RemoteSearches Indexes Stats Wilcard`
- `IndexerLevel - Search Failures`
- `IndexerLevel - Slow peer from remote searches`
- `IndexerLevel - strings_metadata triggering bucket rolling`
- `MonitoringConsole - Check OS ulimits via REST`
- `MonitoringConsole - Core dumps have appeared on the filesystem`
- `MonitoringConsole - Crash logs have appeared on the filesystem`
- `SearchHeadLevel - authorize.conf settings will prevent some users from appearing in the UI`
- `SearchHeadLevel - Captain Switchover Occurring`
- `SearchHeadLevel - Dashboards invalid character in splunkd`
- `SearchHeadLevel - Dashboards using special characters`
- `SearchHeadLevel - Dashboards with all time searches set`
- `SearchHeadLevel - datamodel errors in splunkd`
- `SearchHeadLevel - Detect bundle pushes no longer occurring`
- `SearchHeadLevel - Detect Excessive Search Use - Dashboard - Automated`
- `SearchHeadLevel - Detect MongoDB errors`
- `SearchHeadLevel - Detect searches hitting corrupt buckets`
- `SearchHeadLevel - dispatch metadata files may need removal`
- `SearchHeadLevel - Excessive REST API usage`
- `SearchHeadLevel - KVStore Or Conf Replication Issues Are Occurring`
- `SearchHeadLevel - platform_stats access summary`
- `SearchHeadLevel - platform_stats.audit metrics api`
- `SearchHeadLevel - platform_stats.audit metrics searches`
- `SearchHeadLevel - platform_stats.audit metrics users`
- `SearchHeadLevel - platform_stats.audit metrics users 24hour`
- `SearchHeadLevel - platform_stats.remote_searches metrics populating search`
- `SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search`
- `SearchHeadLevel - platform_stats.users dashboards`
- `SearchHeadLevel - platform_stats.users savedsearches`
- `SearchHeadLevel - RMD5 to savedsearch_name lookupgen report`
- `SearchHeadLevel - savedsearches invalid character in splunkd`
- `SearchHeadLevel - SavedSearches using special characters`
- `SearchHeadLevel - Scheduled Searches That Cannot Run`
- `SearchHeadLevel - Script failures in the last day`
- `SearchHeadLevel - Search Messages admins only`
- `SearchHeadLevel - Search Messages user level`
- `SearchHeadLevel - Search Queries summary exact match`
- `SearchHeadLevel - Search Queries summary non-exact match`
- `SearchHeadLevel - SHC Captain unable to establish common bundle`
- `SearchHeadLevel - Splunk alert actions exceeding the max_action_results limit`
- `SearchHeadLevel - Splunk Scheduler logs have not appeared in the last`
- `SearchHeadLevel - Users exceeding the disk quota`

## KVStore Usage
Some CSV lookups are now replaced with kvstore entries due to the ability to sync the kvstore across multiple search head or search head cluster(s) via apps like [KV Store Tools Redux](https://splunkbase.splunk.com/app/5328/)

## platform_stats reports
There are a number of reports with the keyword "platform_stats" in the title, these were designed to run mcollect commands and to collect data into a metric index
The metrics then contain detailed information around the number of users using Splunk per-search head cluster, data indexed at the indexing tier, resource usage per user et cetera.
There is plenty of detail in here but dashboards were not included for the information built from them, contributions welcome

## Detecting which indexes are searched by Splunk users
As of version 8.0.8 there is still no accurate way to detect which indexes were searched by a user based on their level of access, the audit logs simply do not record which indexes were accessed
Therefore the following searches are part of this app to help achieve this goal:
- `SearchHeadLevel - Search Queries summary exact match`
- `SearchHeadLevel - Search Queries summary non-exact match`

As per the searches description they both require other reports such as `SearchHeadLevel - Macro report`, the description of each search details the various reports they rely on to make them work.

However these complicated searches are not 100% accurate, alternative searches exist in this app to work at the indexing tier:
- `IndexerLevel - RemoteSearches Indexes Stats` 
- `IndexerLevel - RemoteSearches Indexes Stats Wildcard` 

The `remote_searches.log` at the indexing tier does not (usually) need to perform macro substitution but instead you do not have information around the user that ran the searches so this search is more likely to overcount index access than the search tier version, it is also less likely to miss an index due to macro usage or similar...

In more detail, the challenges with the search head level's `audit.log` searches are:
- You cannot determine which index was used if multiple indexes were specified, for example a search such as `index=A OR index=B`, if this search results in more than 0 results, then you cannot be sure which index returned the results so both are recorded by searches in this app
- macros, eventtypes, tags and datamodels are recorded in the `audit.log` so you need to substitute the macro/eventtype/tag to correctly determine if an index is in use, to make this more complicated, macros can be nested so a macro may refer to another macro and the 2nd or 3rd macro may contain the `index=` information
- There are many ways to search an index, such as `index= ""`, `index IN (...)`, the regex'es attempt to deal with the various straightforward scenarios such as `NOT index=A index=B`, but it is not straightforward to correctly extract index names from the `audit.log` in all scenarios
- The `audit.log` information for ad-hoc searches does not record app-context, therefore even if you know the macro and user information, you cannot be sure which app the search was run from and therefore you cannot correctly substitute the macro/tag/eventtype information
- The queries I have built search for a `scan_count` of > 0, this way index=randomstring doesn't appear as an index access, however if a search is trying to use a valid index and the `scan_count` is 0 the search is not counted (this would likely be an edge case)...

At the indexing tier the `remote_searches.log` file has different challenges:
- While macros, eventtypes and tags are expanded (in most cases, there are bugs that allow macros to reach the indexing tier), you instead lose the user context in cases such as ad-hoc searches. This means that a search like `index=*` run by a user with permissions to access 1 index to these searches will appear to be accessing all indexes. The current implementation of the RemoteSearches queries in this app assume access to all indexes if the username is unknown (which may result in excess matching rather than missing searches)
- app context is again missing for ad-hoc searches, although this is less important at the indexing tier
- You cannot determine which index was used if multiple indexes were specified, for example a search such as `index=A OR index=B`, if this search results in more than 0 results, then you cannot be sure which index returned the results so both are recorded by searches in this app
- If the log line is very long it is truncated with a message similar to ...{skipping 46464 bytes}..., this often results in the last index= in the log getting truncated and also some index= strings from the search will not appear in the logs (for example in a datamodel acceleration search with many indexes listed)
- Note that searches with a `scan_count` of 0 are counted, there is an additional metric to measure scan count if you wish to find only indexes that are scanning more than 0 data

Either way the search head level version seems to be "good enough" to determine who is searching which index in most cases, the RemoteSearches queries cover some of the edge cases but the count will generally be higher than expected, the below ideas require more votes if these issues are important to you.

The following ideas relate to this issue:
[Better audit logs](https://ideas.splunk.com/ideas/E-I-49)
[Provide index access statistics to assist in capacity planning of the indexing tier](https://ideas.splunk.com/ideas/E-I-38)

## Which searches require the TA-Alerts for SplunkAdmins add-on?
- `IndexerLevel - RemoteSearches Indexes Stats Wilcard`
- `SearchHeadLevel - Search Queries summary non-exact match`
- `SearchHeadLevel - Dashboards using depends and running searches in the background`

## Feedback?
Feel free to open an issue on github or use the contact author on the SplunkBase link and I will try to get back to you when possible, thanks!

## Release Notes
### 3.0.2
Merged pull request from jeffland-consist via github including various changes

New alerts:
- `IndexerLevel - replicationdatareceiverthread close to 100% utilisation`

New macros:
- `splunkadmins_metrics_source`
- `splunkadmins_hec_metrics_source`

New reports:
- `SearchHeadLevel - Accelerated DataModels Access Info`
- `SearchHeadLevel - Dashboards resulting in concurrency issues`
- `SearchHeadLevel - Dashboards that may benefit from base or post-process searches`
- `SearchHeadLevel - Searches by search type`

Updated macros:
- `splunkadmins_splunkd_source`
- `splunkadmins_splunkuf_source`
- `splunkadmins_mongo_source`
- `splunkadmins_license_usage_source`

To include a trailing wildcard (so splunkd.log.1 matches or similar)

Updated alerts:
- `AllSplunkEnterpriseLevel - Core Dumps Disabled` - updated matching criteria
- `AllSplunkEnterpriseLevel - Non-existent roles are assigned to users` - updated matching criteria
- `AllSplunkEnterpriseLevel - Splunk Servers throwing runScript errors` - updated matching criteria
- `AllSplunkEnterpriseLevel - sendmodalert errors` - updated matching criteria
- `AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - updated matching criteria
- `AllSplunkEnterpriseLevel - Splunk Servers with resource starvation` - updated to use `splunkadmins_splunkd_source` macro
- `AllSplunkLevel - No recent metrics.log data` - corrected comment to be after tstats, updated to use `splunkadmins_metrics_source` macro
- `AllSplunkLevel - DeploymentServer Application Installation Error` - updated matching criteria
- `DeploymentServer - Application Not Found On Deployment Server` - updated matching criteria
- `ForwarderLevel - Channel churn issues` - updated to use `splunkadmins_metrics_source` macro
- `ForwarderLevel - Forwarders connecting to a single endpoint for extended periods` - updated to use `splunkadmins_metrics_source` macro
- `ForwarderLevel - Forwarders connecting to a single endpoint for extended periods UF level` - updated to use `splunkadmins_metrics_source` macro
- `ForwarderLevel - Splunk HTTP Listener Overwhelmed` - updated matching criteria
- `ForwarderLevel - Splunk Universal Forwarders Exceeding the File Descriptor Cache` - updated matching criteria
- `ForwarderLevel - Splunk Universal Forwarders that are time shifting` - updated matching criteria
- `ForwarderLevel - Stopping all listening ports` - updated to use `splunkadmins_splunkd_source` macro
- `IndexerLevel - Buckets changes per day` - updated matching criteria, updated to use `splunkadmins_splunkd_source` macro
- `IndexerLevel - Indexer Queues May Have Issues` - updated to use `splunkadmins_metrics_source` macro
- `IndexerLevel - Knowledge bundle upload stats` - updated to use `splunkadmins_metrics_source` macro
- `IndexerLevel - platform_stats.indexers totalgb_thruput measurement` - updated to use `splunkadmins_metrics_source` macro
- `IndexerLevel - platform_stats.indexers stddev measurement` - updated to use `splunkadmins_metrics_source` macro
- `IndexerLevel - platform_stats.indexers stddev incoming measurement` - updated to use `splunkadmins_metrics_source` macro
- `IndexerLevel - Weekly Broken Events Report` - updated matching criteria
- `IndexerLevel - Time format has changed multiple log types in one sourcetype` - updated matching criteria
- `IndexerLevel - Buckets have being frozen due to index sizing` - updated matching criteria
- `IndexerLevel - Unclean Shutdown - Fsck` - updated matching criteria
- `IndexerLevel - Index not defined` - updated matching criteria
- `IndexerLevel - Timestamp parsing issues combined alert` - updated to use `splunkadmins_splunkd_source` macro
- `IndexerLevel - S2SFileReceiver Error` - updated matching criteria
- `MonitoringConsole - Core dumps have appeared on the filesystem` - corrected to use `indexer_cluster_name` macro
- `MonitoringConsole - Crash logs have appeared on the filesystem` - corrected description
- `SearchHeadLevel - LDAP users have been disabled or left the company cleanup required` - updated matching criteria
- `SearchHeadLevel - Long filenames may be causing issues` - updated matching criteria
- `SearchHeadLevel - SHCluster Artifact Replication Issues` - updated matching criteria
- `SearchHeadLevel - Captain Switchover Occurring` - updated matching criteria
- `SearchHeadLevel - Knowledge bundle replication times metrics.log` - updated to use `splunkadmins_metrics_source` macro
- `SearchHeadLevel - Detect bundle pushes no longer occurring` - updated to use `splunkadmins_metrics_source` macro
- `SearchHeadLevel - WLM aborted searches` - updated matching criteria
- `SearchHeadLevel - SHC Captain unable to establish common bundle` - updated to use `splunkadmins_splunkd_source` macro

Updated dashboards:
- `ClusterMasterJobs.xml`
- `heavyforwarders_max_data_queue_sizes_by_name.xml`
- `heavyforwarders_max_data_queue_sizes_by_name_v8.xml`
- `hec_performance.xml`
- `indexer_data_spread.xml`
- `indexer_max_data_queue_sizes_by_name.xml`
- `indexer_max_data_queue_sizes_by_name_v8.xml`
- `rolled_buckets_by_index.xml`
- `smartstore_stats.xml`
- `splunk_forwarder_data_balance_tuning.xml`
- `splunk_forwarder_output_tuning.xml`

To use `splunkadmins_splunkd_source` and/or `splunkadmins_metrics_source` macros

### 3.0.1
New macros:
- `splunkadmins_shutdown_time_by_period`

New alerts:
- `MonitoringConsole - Check OS ulimits via REST`
- `SearchHeadLevel - Detect bundle pushes no longer occurring`

New reports:
- `DeploymentServer - Count by application` - contributed by @trex (radler)
- `IndexerLevel - DataModel Acceleration - Indexes in use`
- `SearchHeadLevel - Knowledge bundle status on indexers`
- `SearchHeadLevel - Knowledge bundle replication times metrics.log`

Updated alerts:
- `AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only`

Updated dashboards:
- `splunk_introspection_io_stats` - updated names/description of fields used
- `indexer_max_data_queue_sizes_by_name` - minor tweak to replication queue queries 
- `indexer_max_data_queue_sizes_by_name_v8` - minor tweak to replication queue queries
- `splunk_forwarder_output_tuning` - comment update only

Updated macros:
- `splunkadmins_shutdown_time_by_period(4)` to work as expected

Added link to Admins Little Helper for Splunk and TrackMe
README.md improvements 

### 3.0.0

Due to the creation of TA-Alerts for SplunkAdmins, the following are removed in this release:
- bin directory
- README directory
- default/searchbnf.conf
- default/inputs.conf
- default/commands.conf

LookupWatcher and the custom commands streamfilter and streamfilterwildcard are now moved into the new TA-Alerts for SplunkAdmins application

New alerts:
- `AllSplunkEnterpriseLevel - error in stdout.log`
- `IndexerLevel - platform_stats.indexers stddev incoming measurement` 
- `MonitoringConsole - Core dumps have appeared on the filesystem` 
- `MonitoringConsole - Crash logs have appeared on the filesystem`
- `SearchHeadLevel - Splunk Scheduler logs have not appeared in the last`

Updated:
- `AllSplunkEnterpriseLevel - Replication Failures` - simplified criteria to match more issues
- `AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - corrected order of statements so this works as expected, added 1 more exclusion
- `IndexerLevel - platform_stats.indexers stddev measurement` - narrowed down to sourcetype/source
- `IndexerLevel - Search Failures` - changed criteria
- `IndexerLevel - Indexer Queues May Have Issues` - added server count
- `IndexerLevel - RemoteSearches Indexes Stats Wilcard` - description update as this requires TA-Alerts for SplunkAdmins
- `SearchHeadLevel - Dashboards using depends and running searches in the background` - description update as this requires TA-Alerts for SplunkAdmins
- `SearchHeadLevel - Detect MongoDB errors` - excluded 1 warning
- `SearchHeadLevel - Search Queries summary exact match` - comment update
- `SearchHeadLevel - Search Queries summary non-exact match` - comment and description update as this requires TA-Alerts for SplunkAdmins
- `SearchHeadLevel - Search Messages user level` - removed "DAG Execution Exception"
- `SearchHeadLevel - Search Messages admins only` - excluded "Found no results to append to collection"

### 2.6.13
Updated python SDK to 1.6.20

Updates to reports/alerts:
`IndexerLevel - Future Dated Events that appeared in the last week` - comment upate

`IndexerLevel - IndexConfig Warnings from Splunk indexers` - added wildcard to improve matching

Updated regex to handle index:: case:
`IndexerLevel - RemoteSearches Indexes Stats`

`IndexerLevel - RemoteSearches Indexes Stats Wilcard`

`SearchHeadLevel - Determine query scan density`

`SearchHeadLevel - Search Queries By Type Audit Logs`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version other`

`SearchHeadLevel - SmartStore cache misses - dashboards`

`SearchHeadLevel - SmartStore cache misses - savedsearches`

`SearchHeadLevel - SmartStore cache misses - combined`

Updated regex to handle index:: case: and minor tweak to replace comments with spaces:
`SearchHeadLevel - Search Queries summary exact match`

`SearchHeadLevel - Search Queries summary non-exact match`

Updated links in nav menu:
[SideView UI (user activity)](https://splunkbase.splunk.com/app/6449/)

### 2.6.12
Correct typo in savedsearches.conf (a missing \ character), (feedback from Vincent) 

### 2.6.11
New dashboards:
`splunk_introspection_io_stats` - just an I/O focussed dashboard based on introspection data

New macro:
`splunkadmins_shutdown_time_by_shc`

`cluster_masters`


Updated alerts:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - more criteria

`IndexerLevel - IndexConfig Warnings from Splunk indexers` - updated criteria, using stats instead of top

`SearchHeadLevel - KVStore Or Conf Replication Issues Are Occurring` - updated keywords for new instances, added more criteria to reduce false alarms

`SearchHeadLevel - Lookup updates within SHC` - changed to addCommit instead of acceptPush

Updated dashboards:
`heavyforwarders_max_data_queue_sizes_by_name_v8` - corrected missing space in "TcpOut KB per second per forwarder" panel, (feedback from Vincent)

`indexer_max_data_queue_sizes_by_name` - updated comment on replication queue, replication queue issues now show duration

`smartstore_stats` - updated comment

`splunk_forwarder_output_tuning` - added attribution as the link is available via search engines and public, updated comments

Changed:
`splunkadmins_userlist_indexinfo` into a csv file to prevent unncessary restarts related to updating this app (on standalone instances this triggers a restart due to collections.conf), collections.conf was removed from this app

### 2.6.10
README.md update

New alert:
`SearchHeadLevel - Excessive REST API usage`

New dashboard:
`splunk_forwarder_data_balance_tuning` - new dashboard based on Brett Adam's work

New macro:
`diskusage`

Updated alert:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - more criteria

`ForwarderLevel - Channel churn issues` - added another TERM to the search, added stats line to summarise the result, added to where so this fires only if channels added and removed

`IndexerLevel - RemoteSearches Indexes Stats` - updated comment and rename of fields

`IndexerLevel - RemoteSearches Indexes Stats Wilcard` - updated comment and rename of fields

`SearchHeadLevel - Detect MongoDB errors` - regex update to remove false positives

`SearchHeadLevel - Indexer Peer Connection Failures` - updated comment and sourcetype

`SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search` - added rounding of fields, updated comment

`SearchHeadLevel - platform_stats.users savedsearches` - added time field

`SearchHeadLevel - platform_stats.users dashboards` - added time field

`SearchHeadLevel - Scheduled Searches That Cannot Run` - corrected failure count so it's accurate

`SearchHeadLevel - Search Messages user level` - more criteria and excluded some warnings

`SearchHeadLevel - Search Queries summary exact match` - updates to stats to include 1 more field, updated regex to match macros in multisearch commands, updated comment, removed extra ' character from search field

`SearchHeadLevel - Search Queries summary non-exact match` - updated comment, updated regex to match macros in multisearch commands, removed extra ' character from search field

Updated dashboards:
`hec_performance` - to include the additional `num_of_requests_waiting_ack` measurement from introspection data, if this is high it can stop data when tokens have useACK set to true

`smartstore_stats` - various new panels around queueing of downloads, and other potential smartstore issues

`splunk_forwarder_output_tuning` - update to include another measure of data balance

Updated comments on alerts:
`AllSplunkLevel - Unable To Distribute to Peer`

`SearchHeadLevel - splunk_search_messages dispatch` - description update

Updated metadata file to allow `sc_admin` role access

### 2.6.9
Updated alerts:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - removed 1 log entry for consecutive date entries/unretrievable data

`ForwarderLevel - Splunk HEC issues` - added cluster command

New dashboards:
`ForwarderLevel - Splunk HEC issues`

New reports:
`IndexerLevel - SmartStore cache misses - remote_searches`

`IndexerLevel - Buckets in cache`

`SearchHeadLevel - Detect searches hitting corrupt buckets`

`SearchHeadLevel - SmartStore cache misses - savedsearches`

`SearchHeadLevel - SmartStore cache misses - dashboards`

`SearchHeadLevel - SmartStore cache misses - combined`

Updated SDK to 1.6.18

Updated alerts/reports to remove unncessary `TERM()` commands:
`AllSplunkEnterpriseLevel - Losing Contact With Master Node`

`AllSplunkEnterpriseLevel - Replication Failures`

`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only`

`ForwarderLevel - Splunk HEC issues` - included lookup file to translate the HTTP code seen by client (based on the documentation version 8.2.3)

`IndexerLevel - Data parsing error`

`IndexerLevel - IndexWriter pause duration`

`IndexerLevel - RemoteSearches Indexes Stats`

`IndexerLevel - RemoteSearches Indexes Stats Wilcard`

`IndexerLevel - RemoteSearches find all time searches`

`IndexerLevel - RemoteSearches find datamodel acceleration with wildcards`

`IndexerLevel - Slow peer from remote searches`

`SearchHeadLevel - Dashboards invalid character in splunkd`

`SearchHeadLevel - platform_stats.remote_searches metrics populating search`

`SearchHeadLevel - savedsearches invalid character in splunkd`

`SearchHeadLevel - Script failures in the last day`

`SearchHeadLevel - Search Messages field extractor slow`

`SearchHeadLevel - Search Messages user level`

`SearchHeadLevel - Search Messages admins only`

### 2.6.8
New alerts:
`AllSplunkLevel - No recent metrics.log data`

New dashboards:
`heavyforwarders_max_data_queue_sizes_by_name_v8` - this version uses tstats with PREFIX so only works with Splunk 8.0+

`indexer_max_data_queue_sizes_by_name_v8` - this version uses tstats with PREFIX so only works with Splunk 8.0+

`splunk_forwarder_output_tuning` - using metrics.log to measure the TCP output/stdev per-name, includes example tuning parameters

New reports:
`IndexerLevel - platform_stats.indexers stddev measurement` - stdev per indexer cluster (useful for tuning the outputs.conf from incoming servers)

`IndexerLevel - platform_stats.indexers totalgb_thruput measurement` - index thruput measurements

Updated alerts:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - more alert criteria

`IndexerLevel - Cold data location approaching size limits` - improvements to calculation of % used

`IndexerLevel - Data parsing error` - added macro `splunkadmins_dataparsing_error` as requested

`SearchHeadLevel - Realtime Scheduled Searches are in use` - updated timeout to 900 seconds, added context to description about potential use (as per feedback from Vincent)

`SearchHeadLevel - Script failures in the last day` - improved user id matching

`SearchHeadLevel - Search Messages admins only` - more alert criteria

`SearchHeadLevel - Search Messages user level` - more alert criteria

Updated macros:
`splunkadmins_shutdown_keyword` - updated keyword for shutdown state

`splunkadmins_shutdown_list` - updated keyword for shutdown state

`splunkadmins_shutdown_time` - updated keyword for shutdown state

Updated reports:
`IndexerLevel - platform_stats.counters hosts` - updated to use `indexer_cluster_name` macro

`IndexerLevel - platform_stats.counters hosts 24hour` - updated to use `indexer_cluster_name` macro

`IndexerLevel - platform_stats.indexers totalgb measurement` - updated to use `indexer_cluster_name` macro, comment update

`IndexerLevel - RemoteSearches find datamodel acceleration with wildcards` - handling the IN clause in `remote_searches.log`

`IndexerLevel - RemoteSearches Indexes Stats` - added short field

`IndexerLevel - RemoteSearches Indexes Stats` - added short field (set to False), to make queries easier

`SearchHeadLevel - platform_stats.users dashboards` - updated mcollect comment

`SearchHeadLevel - Search Messages user level` - added more error messages, limited the message to the first 30 messages

`SearchHeadLevel - Search Messages admins only` - added more error messages

`SearchHeadLevel - Search Queries summary exact match` - excluded Remote storage searches (no real difference)

`SearchHeadLevel - Search Queries summary non-exact match` - excluded Remote storage searches (no real difference)

### 2.6.7
New alerts:
`IndexerLevel - SmartStore - Bucket cache errors audit logs`

`SearchHeadLevel - Accelerated DataModels with wildcard or no index specified`

New reports:
`IndexerLevel - IndexWriter pause duration`

`IndexerLevel - RemoteSearches find all time searches`

`IndexerLevel - RemoteSearches find datamodel acceleration with wildcards`

`SearchHeadLevel - platform_stats.audit metrics users 24hour`

`SearchHeadLevel - platform_stats.users dashboards`

`SearchHeadLevel - platform_stats.users savedsearches`

Updated alerts:
`AllSplunkEnterpriseLevel - sendmodalert errors` - updated to refer to `SearchHeadLevel - Script failures in the last day` as it replaces most of this alerts functionality...

`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - more alert criteria

`DeploymentServer - Error Found On Deployment Server`

`SearchHeadLevel - audit logs showing all time searches` - minor correction to display all searches without a `savedsearch_name`

`SearchHeadLevel - Accelerated DataModels with All Time Searching Enabled` - re-wrote the search to not use map

`SearchHeadLevel - Script failures in the last day` - updated to handle various webhook failures

Updated reports:
`IndexerLevel - RemoteSearches Indexes Stats` - updates to work with search heads with _ in the name, improved handling of "skipped" entries

`IndexerLevel - RemoteSearches Indexes Stats Wilcard` - updates to work with search heads with _ in the name, improved handling of "skipped" entries

`SearchHeadLevel - Search Queries summary non-exact match` - new field "short", updated regex

`SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search` - updates to work with search heads with _ in the name

`SearchHeadLevel - platform_stats.remote_searches metrics populating search` - updates to work with search heads with _ in the name


### 2.6.6
Updated to Splunk python SDK 1.1.16

Merged from jordanfelle to fix special character

Updated alerts:
`SearchHeadLevel - dispatch metadata files may need removal`

`SearchHeadLevel - Dashboards with all time searches set`

### 2.6.5
New reports:
`IndexerLevel - RemoteSearches Indexes Stats Wilcard` - example wildcard match for remote_searches.log

`SearchHeadLevel - Index list by cluster report` - for a list of indexes by indexer cluster

Updated reports:
`IndexerLevel - RemoteSearches Indexes Stats` - added additional info around bucket cache usage, improved accuracy, provided mcollect example

`IndexerLevel - Slow peer from remote searches` - added more search types into the list

`SearchHeadLevel - Search Queries summary exact match` - improved accuracy for append/join/multisearch/set

`SearchHeadLevel - Search Queries summary non-exact match` - improved accuracy for append/join/multisearch/set

Updated alerts:
`AllSplunkEnterpriseLevel - Splunk Servers with resource starvation` - as per github issue #12, thanks RahimAbdulla

`SearchHeadLevel - Detect MongoDB errors` - fix the alert by re-adding the fillnull into the subsearch

Updated alerts/reports with new search macro for audit logs:
`SearchHeadLevel - Users with auto-finalized searches`

`SearchHeadLevel - Search Queries By Type Audit Logs`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version other`

`SearchHeadLevel - Detect Excessive Search Use - Dashboard - Automated`

`SearchHeadLevel - platform_stats.audit metrics searches`

`SearchHeadLevel - platform_stats.audit metrics users`

`SearchHeadLevel - Searches dispatched as owner by other users`

Updated alerts/reports with (?s) as some logs are now multi-line in 8.2.x (updating just in case):
`SearchHeadLevel - Scheduled searches not specifying an index`

`SearchHeadLevel - User - Dashboards searching all indexes`

`SearchHeadLevel - Realtime Search Queries in dashboards`

`SearchHeadLevel - Scheduled searches not specifying an index macro version`

`SearchHeadLevel - User - Dashboards searching all indexes macro version`

`SearchHeadLevel - Determine query scan density`

`SearchHeadLevel - Users with auto-finalized`

`SearchHeadLevel - Scheduled searches status`

`SearchHeadLevel - Dashboard refresh intervals`

Updated macros:
`splunkadmins_audit_logs_macro_sub_v8` - to work in more cases (more output but less chance of missing a macro)

Updated all dashboards to include the version="1.1" tag as required for new Splunk versions

### 2.6.4
Updated alerts:
`AllSplunkLevel - Splunk forwarders that are not talking to the deployment server` - contribution via email (Vincent)

`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - a few new additions

`SearchHeadLevel - datamodel errors in splunkd` - excluded kvstore shutdown

`SearchHeadLevel - Search Messages admins only` - new exclusions

Updated dashboard:
`issues_per_sourcetype` - the `Invalid parsed time` panel needed another regex - contribution via email (Vincent)

Updated reports:
`SearchHeadLevel - Search Queries summary exact match` - minor updates, added cache stats, improved accuracy

`SearchHeadLevel - Search Queries summary non-exact match` - minor updates, added cache stats, improved accuracy

Renamed/replaced reports:
`SearchHeadLevel - Search Queries summary exact match 73` - new name is `SearchHeadLevel - Search Queries summary exact match`

`SearchHeadLevel - Search Queries summary non-exact match 73 ` - new name is `SearchHeadLevel - Search Queries summary non-exact match`

`SearchHeadLevel - Search Queries summary exact match 73 by user` - new name is `SearchHeadLevel - Search Queries summary exact match by user`

`SearchHeadLevel - Search Queries summary exact match 73 by index` - new name is `SearchHeadLevel - Search Queries summary exact match by index`

Updates to:
`streamfilter.py` - correct utf-8 error python 3

`streamfilterwildcard.py` - correct utf-8 error python 3


### 2.6.3
New alert:
`SearchHeadLevel - authorize.conf settings will prevent some users from appearing in the UI`

Updated alerts:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - a few more errors

`SearchHeadLevel - Search Messages user level` - updated comment, added sid field

`SearchHeadLevel - Search Messages admins only` - added sid field

`SearchHeadLevel - Detect MongoDB errors` - added partial flag to remove false alarms (thanks afx)

`IndexerLevel - Timestamp parsing issues combined alert` - update to provide a list of hosts per sourcetype

Updated dashboards:
`detect_excessive_search_use` - removing ldap query section (as this is env specific)

`issues_per_sourcetype` - wording update on title

`knowledge_objects_by_app` - corrected drilldown link to point to the SplunkAdmins app (thanks Vincent!)


Updated Splunk python SDK to 1.6.15 

### 2.6.2
Identical to 2.6.1, re-released to get around automated app inspect failure

### 2.6.1
2 navigation menu items fixed (incorrect alert names) by pull request from EsOsO

New alerts:
`SearchHeadLevel - Splunk alert actions exceeding the max_action_results limit` - detect if any alert action exceeds the limit and receives limited results, currently a silent failure as per https://ideas.splunk.com/ideas/EID-I-781

Updated alerts:
`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` - exclusion for config reload requiring restart

`IndexerLevel - Search Failures` - comment/description update only (replaced by search messages based alerts)

`SearchHeadLevel - Detect MongoDB errors` - added missing | symbol as per email update from afx

`SearchHeadLevel - Search Messages user level` - excluded messages from kvstore initialization and a few others, added macros

`SearchHeadLevel - Search Messages admins only` - added messages for kvstore unknown status and a few others, added macros

`SearchHeadLevel - SHC Captain unable to establish common bundle` - excluded indexer shutdown times

`SearchHeadLevel - Splunk alert actions exceeding the max_action_results limit` - now ignores emails with no results inline (alert now joins with savedsearch info via map), added macro

### 2.6.0
Various README.md updates

New alerts:

`AllSplunkEnterpriseLevel - Splunkd Log Messages Admins Only` this generic alert is designed to capture a variety of splunkd log messages that warrant further investigation or show an issue exists that should be fixed. This alert is generic and captures many errors.

`DeploymentServer - Error Found On Deployment Server` this alert captures deployment server errors, this is more generic than the current alert and designed to catch more scenarios

`SearchHeadLevel - Dashboards invalid character in splunkd` this alert finds errors in splunkd related to invalid characters in a dashboard

`SearchHeadLevel - savedsearches invalid character in splunkd` this alert finds errors in splunkd related to invalid characters in a saved search

`SearchHeadLevel - datamodel errors in splunkd` this alert finds errors related to data models in the splunkd logs

`SearchHeadLevel - Search Messages user level` this alert is designed to be combined with an app like sendresults.
This searches the splunk search messages and looks for errors that should be actionable by a end user
This is designed to be a generic alert covering many failure scenarios

`SearchHeadLevel - Search Messages admins only` this alert searches the splunk search messages but is designed to find errors that cannot be fixed by end users, the user level version is for end user level errors

New lookup file:

`splunkadmins_rmd5_to_savedsearchname.csv`

New reports:

`SearchHeadLevel - RMD5 to savedsearch_name lookupgen report` new helper report for translating rmd5 names in the search id back to a report name.

`SearchHeadLevel - Search Messages field extractor slow` looks for messages about a slow field extractor in the splunk search messages

Updated macro:

`search_type_from_sid` to work with real-time searches 

Updated alerts:

`AllSplunkLevel - Application Installation Failures From Deployment Manager` updated to handle download failures and use cluster command

`AllSplunkEnterpriseLevel - Email Sending Failures` updated to work on logging changes in 8.0.x

`AllSplunkEnterpriseLevel - Splunk Servers throwing runScript errors` updated to work on logging changes in 8.0.x
 
`AllSplunkEnterpriseLevel - Splunk Servers with resource starvation` now includes an additional error/warning message

`AllSplunkEnterpriseLevel - Replication Failures` now includes more types of knowledge bundle replication issues and uses cluster command

`IndexerLevel - IndexConfig Warnings from Splunk indexers` updated to include error level messages 

`IndexerLevel - Slow peer from remote searches` updated to remove special double quote characters

`IndexerLevel - Peer will not return results due to outdated generation` to update description to refer to `AllSplunkEnterpriseLevel - Losing Contact With Master Node `

`IndexerLevel - Data parsing error` now includes csv and json line breaker errors, now uses stats instead of cluster 

`SearchHeadLevel - Script failures in the last day` expanded to handle modular alerts and script errors in one alert. Also attempts to translate base64 or encoded report names back to human readable versions

`SearchHeadLevel - Macro report` updated crontab to all days of the week 

`SearchHeadLevel - Users with auto-finalized searches` description update 

`SearchHeadLevel - Search Queries summary exact match 73` minor update to deal with real-time searches in regex

`SearchHeadLevel - Search Queries summary non-exact match 73` minor update to deal with real-time searches in regex

`SearchHeadLevel - SHC Captain unable to establish common bundle` updated to include one more error/warning message

`SearchHeadLevel - platform_stats access summary` updated to deal with real-time searches in regex

`SearchHeadLevel - Dashboards using special characters` added ignore for trackme and network diagram viz as this was breaking the rex command, also removed an extra rex line 

`SearchHeadLevel - splunk_search_messages dispatch` comment update only 

`SearchHeadLevel - dispatch metadata files may need removal` update to use macro

`SearchHeadLevel - Search Queries summary exact match 73` description/comment update

`SearchHeadLevel - Search Queries summary non-exact match 73` description/comment update

Renamed alert:

`IndexerLevel - Splunk Indexers Losing Contact With Master` to `AllSplunkEnterpriseLevel - Losing Contact With Master Node` alert renamed and now includes search head to master node and indexers to master node in one alert

Removed alert:

`IndexerLevel - Unable to replicate thawed directories in a cluster`

### 2.5.14
Update Splunk python SDK to 1.6.14

New alerts:
`IndexerLevel - Slow peer from remote searches`

Updated dashboard:
`hec_performance` as per pull request from jordanfelle

### 2.5.13
Minor fixes for app inspect (new empty lookup file)

### 2.5.12
New alerts:
`SearchHeadLevel - splunk_search_messages dispatch`

`SearchHeadLevel - WLM aborted searches`

`SearchHeadLevel - dispatch metadata files may need removal`

Minor changes to reports:
`SearchHeadLevel - Search Queries summary exact match 73`

`SearchHeadLevel - Search Queries summary non-exact match 73`

And macro:
`splunkadmins_audit_logs_datamodel_sub`

Updated alert:
`SearchHeadLevel - Dashboards with all time searches set` to look for earliest= in tokens and to ignore that case

Updated reports:
`SearchHeadLevel - Indexer Peer Connection Failures`

`SearchHeadLevel - Detect searches hitting corrupt buckets`

The above were updated to use `splunk_search_messages` sourcetype

`IndexerLevel - Knowledge bundle upload stats` updated to handle cascading bundle replication

### 2.5.11
Added notes around the `log_search_messages` property under [search] in limits.conf

New macros:
`conf_rest_endpoint`

`splunkadmins_epoch`

`splunkadmins_audit_logs_datamodel_sub`

`splunkadmins_audit_logs_eventtypes_sub`

`splunkadmins_audit_logs_macro_sub_v8` - note this version uses mvmap so Splunk v8+, the `splunkadmins_audit_logs_macro_sub` still exists for pre-version 8 but can only replace 1 macro per run...

`splunkadmins_audit_logs_tags_sub`

New reports:
`SearchHeadLevel - DataModels report`

`SearchHeadLevel - Tags report`

`SearchHeadLevel - EventTypes report`

Updated dashboard `troubleshooting_resource_usage_per_user_drilldown` to display the correct time range for more searches

Updated reports:
`IndexerLevel - RemoteSearches Indexes Stats` - to summarize indexes stats

`SearchHeadLevel - Scheduled searches not specifying an index macro version`

`SearchHeadLevel - User - Dashboards searching all indexes macro version`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version`

`SearchHeadLevel - Search Queries By Type Audit Logs macro version other`

`SearchHeadLevel - Dashboards with all time searches set`

To use the new macro `splunkadmins_audit_logs_macro_sub_v8`

Upated reports:
`SearchHeadLevel - Search Queries summary exact match 73`

`SearchHeadLevel - Search Queries summary non-exact match 73`

To use the new macros `splunkadmins_audit_logs_macro_sub_v8`, `splunkadmins_audit_logs_eventtypes_sub`, `splunkadmins_audit_logs_datamodel_sub`, `splunkadmins_audit_logs_tags_sub`


### 2.5.10
Updated to Splunk python SDK 1.6.13 (previous 2.5.9 did not include this update)

New alerts:
`AllSplunkLevel - TailReader Ignoring Path`

`ForwarderLevel - Channel churn issues`

`SearchHeadLevel - Dashboards with all time searches set`

New reports:
`SearchHeadLevel - audit logs showing all time searches`

Updated reports:
`SearchHeadLevel - Macro report` to use the new macro

`SearchHeadLevel - Search Queries summary exact match 73` to use the new macro

`SearchHeadLevel - Search Queries summary non-exact match 73` to use the new macro

New macros:
`splunkadmins_splunk_server_name`

### 2.5.9
New alerts:
`AllSplunkLevel - Unexpected termination of a Splunk process windows`

`AllSplunkLevel - Unexpected termination of a Splunk process unix`

`IndexerLevel - strings_metadata triggering bucket rolling`

New reports:
`ForwarderLevel - Data dropping duration`

`SearchHeadLevel - Lookup CSV size`

New dashboards:
`lookup_audit`

New macro:
`mylookups` (7.3.3+ only)

New nav menu items:
Hyperlink to https://github.com/silkyrich/cluster_health_tools

Updated to Splunk python SDK 1.6.12
Set `python.version = python3` within inputs.conf.spec as per appinspect requirement

### 2.5.8
New alerts:
`ClusterMasterLevel - excess buckets on master`

Updated alerts:
`ForwarderLevel - Splunk HEC issues` - corrected criteria for newer Splunk versions and added more matching in

`SearchHeadLevel - SHC Captain unable to establish common bundle` - to remove special character from comment

Renamed alert:
`IndexerLevel - Buckets are been frozen due to index sizing` to `IndexerLevel - Buckets have being frozen due to index sizing` (as requested by woodcock)

New reports:
`SearchHeadLevel - Dashboards using special characters`

`SearchHeadLevel - SavedSearches using special characters`

### 2.5.7
Moved lib directory to bin/lib (as this does not distribute to the indexers otherwise, sent feedback on https://dev.splunk.com/enterprise/docs/python/sdk-python/howtousesplunkpython/howtocreatemodpy/ so this gets updated)

New macro:

`base64decode` this macro requires decrypt or a similar app to be useful but the searches utilising this will work fine without it...

New reports:
`SearchHeadLevel - platform_stats.audit metrics searches`

`SearchHeadLevel - platform_stats.audit metrics users`

`SearchHeadLevel - platform_stats.audit metrics api`

The above 3 replace `SearchHeadLevel - platform_stats.audit metrics` which is now removed.

New reports continued:

`IndexerLevel - RemoteSearches Indexes Stats`

`SearchHeadLevel - DataModel Fields`

`SearchHeadLevel - Dashboard refresh intervals`

`SearchHeadLevel - Dashboards using depends and running searches in the background`

`SearchHeadLevel - Summary searches using realtime search scheduling`

`SearchHeadLevel - Searches dispatched as owner by other users`

Updated reports:

`SearchHeadLevel - Search Queries summary exact match`

`SearchHeadLevel - Search Queries summary non-exact match`

Minor tweaks to the regex for both the above

`SearchHeadLevel - Search Queries summary exact match 73`

`SearchHeadLevel - Search Queries summary non-exact match 73`

The above now attempt to handle append, join, appendcols, multisearch

Also updated reports:

`SearchHeadLevel - platform_stats.remote_searches metrics populating search` to ignore pretypeahead/copybuckets searches, and default acceleration searches

`SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search` to include indexer cluster as a field

`SearchHeadLevel - Scheduled Searches That Cannot Run` to handle additional failure scenarios

Updated `streamfilter.py`, `lookup_watcher.py` and `streamfilterwildcard.py` so they include the libraries from bin/lib

### 2.5.6
Further updates to the new reports from 2.5.5 relating to platform stats, improved accuracy with identifying dashboard usage vs ad-hoc searches

Updated `SearchHeadLevel - platform_stats access summary` to include searches triggered (which are often coming from dashboard usage)

New report:

`SearchHeadLevel - platform_stats.remote_searches metrics populating search`

Updated reports:

`IndexerLevel - platform_stats.counters hosts`

`IndexerLevel - platform_stats.counters hosts 24hour`

`IndexerLevel - platform_stats.indexers totalgb measurement`

`SearchHeadLevel - SHC conf log summary`

`SearchHeadLevel - platform_stats.audit metrics`

`SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search`

`SearchHeadLevel - platform_stats access summary`

New macro:

`search_type_from_sid`

### 2.5.5
Lookup Watcher now imports six from lib directory (allows this to work on older Splunk versions)
Minor update to props.conf for splunk:search:info as in 7.3 auto-finalized messages are now INFO level

New alert:

`SearchHeadLevel - SHC Captain unable to establish common bundle`

New reports:

`IndexerLevel - platform_stats.counters hosts`

`IndexerLevel - platform_stats.counters hosts 24hour`

`IndexerLevel - platform_stats.indexers totalgb measurement`

`SearchHeadLevel - SHC conf log summary`

`SearchHeadLevel - platform_stats.audit metrics`

`SearchHeadLevel - platform_stats.user_stats.introspection metrics populating search`

`SearchHeadLevel - platform_stats access summary`

Updated dashboard:

`indexer_max_data_queue_sizes_by_name`

New macro:

`search_head_cluster`

### 2.5.4
Re-release of 2.5.3 due to strange issue in SplunkBase

### 2.5.3
Lookup files are now included (zero sized), note that you will need to re-generate them after install if you overwrite the lookups used by some reports...

New macros:

`splunkadmins_audit_logs_macro_sub`

`splunkadmins_remote_macros` (this macro requires TA-webtools), alternatively you can you the Mothership app (SplunkBase)

`splunkadmins_remote_roles` (this macro requires TA-webtools), alternatively you can you the Mothership app (SplunkBase)

New reports:

`SearchHeadLevel - IndexesPerRole Remote Report`

`SearchHeadLevel - IndexesPerRole Report`

`SearchHeadLevel - IndexesPerRole srchIndexesallowed Report`

`SearchHeadLevel - IndexesPerRole srchIndexesdefault Report`

`SearchHeadLevel - Search Queries summary exact match 73`

`SearchHeadLevel - Search Queries summary exact match 73 by user` (uses Search Queries summary exact match 73 as base)

`SearchHeadLevel - Search Queries summary exact match 73 by index` (uses Search Queries summary exact match 73 as base)

`SearchHeadLevel - Search Queries summary non-exact match 73`

`SearchHeadLevel - IndexesPerUser Report`

Updated alerts:

`IndexerLevel - Time format has changed multiple log types in one sourcetype`

`IndexerLevel - Timestamp parsing issues combined alert`

Updated dashboard:

`issues_per_sourcetype`

Updated report:

`Updated report SearchHeadLevel - Macro report`

With new regex due to change in newer Splunk versions (credit to woodcock for the update)


Lookup file `splunkadmins_macros_temp.csv` renamed to `splunkadmins_macros.csv`


Changes for python3 compatability

Updated python SDK to 1.6.11 (from 1.6.6)

### 2.5.2
New modular input - Lookup Watcher - details in the README.md file
Introduced a new sub-menu in the navigation menu for Search Head Level "Recommended (externally hosted)" with links to external dashboards 

Updated reports:
`SearchHeadLevel - Search Queries By Type Audit Logs`
`SearchHeadLevel - Search Queries By Type Audit Logs macro version`
`SearchHeadLevel - Search Queries By Type Audit Logs macro version other`

To reduce the number of unknown queries

Updated reports:
`SearchHeadLevel - Search Queries summary exact match`
`SearchHeadLevel - Search Queries summary non-exact match`

To improve the statistics around indexes found

### 2.5.1
Updated alert - `SearchHeadLevel - Scheduled Searches That Cannot Run` tweak to find more results

Updated dashboard `issues per sourcetype` to handle message becoming event_message in newer Splunk versions (7.1 or 7.2)

Updated macros `splunkadmins_shutdown_list`, `splunkadmins_shutdown_keyword`, `splunkadmins_shutdown_time`, `splunkadmins_transfer_captain_times` to handle message becoming event_message in newer Splunk versions (7.1 or 7.2)

Updated python files streamfilter/streamfilterwildcard to import lib relative to the current app name

Updated alerts / reports:
 - `AllSplunkLevel execprocessor errors`
 - `AllSplunkLevel - TCP Output Processor has paused the data flow`
 - `AllSplunkEnterpriseLevel - Detect LDAP groups that no longer exist`
 - `AllSplunkEnterpriseLevel - Email Sending Failures`
 - `AllSplunkEnterpriseLevel - File integrity check failure`
 - `AllSplunkEnterpriseLevel - Non-existent roles are assigned to users`
 - `AllSplunkEnterpriseLevel - Replication Failures`
 - `AllSplunkEnterpriseLevel - TCP or SSL Config Issue`
 - `AllSplunkEnterpriseLevel - Unable to dispatch searches due to disk space`
 - `DeploymentServer - btool validation failures occurring on deployment server`
 - `DeploymentServer - Unsupported attribute within DS config`
 - `ForwarderLevel - crcSalt or initCrcLength change may be required`
 - `ForwarderLevel - Splunk Universal Forwarders Exceeding the File Descriptor Cache`
 - `IndexerLevel - Buckets are been frozen due to index sizing`
 - `IndexerLevel - IndexConfig Warnings from Splunk indexers`
 - `IndexerLevel - Index not defined`
 - `IndexerLevel - Peer will not return results due to outdated generation`
 - `IndexerLevel - Time format has changed multiple log types in one sourcetype`
 - `IndexerLevel - Too many events with the same timestamp`
 - `IndexerLevel - Valid Timestamp Invalid Parsed Time`
 - `SearchHeadLevel - KVStore Or Conf Replication Issues Are Occurring`
 - `SearchHeadLevel - LDAP users have been disabled or left the company cleanup required`
 - `SearchHeadLevel - Scheduled Searches That Cannot Run`
 - `SearchHeadLevel - Scheduled searches failing in cluster with 404 error`
To handle message becoming event_message in newer Splunk versions (7.1 or 7.2)

### 2.5.0
New dashboard `HEC Performance` (original from [camrunr's github](https://github.com/camrunr/hec_perf_report/blob/master/hec_perf_report.xml))

New macro - `splunkadmins_shutdown_keyword`

New report - `IndexerLevel - Knowledge bundle upload stats`

Updated alert - `AllSplunkEnterpriseLevel - Replication Failures` with new criteria and excluded shutdowns

Updated alert - `AllSplunkEnterpriseLevel - Splunk Scheduler skipped searches and the reason` to handle another skipped scenario

Updated alert - `AllSplunkEnterpriseLevel - Splunk Servers with resource starvation` with new comments 

Updated alert - `SearchHeadLevel - Detect MongoDB errors` with update to handle tstats issue in Splunk (issue #3 in github)

Moved splunklib into "lib" directory of app as per updated appinspect recommendations

### 2.4.9
Updated alert - `SearchHeadLevel - Detect MongoDB errors` to include " W " based on git feedback

### 2.4.8
New alert - `ForwarderLevel - Splunk HEC issues`

New dashboard - `Lookups in use finder`

New macro - `splunkadmins_license_usage_source`

New report - `IndexerLevel - Maximum memory utilisation per search`

New report - `SearchHeadLevel - Lookup updates within SHC`

New report - `SearchHeadLevel - Maximum memory utilisation per search`

New report - `SearchHeadLevel - Detect Excessive Search Use - Dashboard - Automated`

Updated alert - `AllSplunkEnterpriseLevel - Replication Failures` to match more results

Updated alert - `ForwarderLevel - Splunk HTTP Listener Overwhelmed` comment/description update

Updated dashboard - `Rolled buckets by index` - to no longer hardcode Linux paths to the license usage log

Updated dashboard - `Heavy Forwarders Max Data Queue Sizes by name` to use the thruput in the metrics.log

### 2.4.7
New README (README.md replaces README)
New dashboard `Detect excessive search usage`
New dashboard `Cluster Master Jobs`
New dashboard `Knowledge Objects by app` (and drilldown dashboard)
New report - `IndexerLevel - Corrupt buckets via DBInspect`
New report - `SearchHeadLevel - Detect changes to knowledge objects`
New report - `SearchHeadLevel - Detect changes to knowledge objects directory`
New report - `SearchHeadLevel - Detect changes to knowledge objects non-directory`
Updated alert `ForwarderLevel - Splunk Universal Forwarders Exceeding the File Descriptor Cache` (comment update)
Updated alert `IndexerLevel - Uneven Indexed Data Across The Indexers` to handle a varying number of indexers
Updated various reports to include the `splunkadmins_restmacro`, this ensures `splunk_server=local` is used where appropriate
Updated dashboard `heavyforwarders_max_data_queue_sizes_by_name`, now has a filter for hosts to look at, corrected TCPOut KB per second panel
Updated macro `splunkadmins_splunkd_source` now defaults to `*splunkd.log` (previously `/opt/splunk/var/log/splunk/splunkd.log`)
Updated macro `splunkadmins_mongo_source` now defaults to `*mongod.log` (previously `/opt/splunk/var/log/splunk/mongod.log`)
Updated report `SearchHeadLevel - Search Queries summary exact` to remove the mvexpand and selfjoin (replaced by stats)

### 2.4.6
New alert - AllSplunkLevel - Data Loss on shutdown
New macro - whataccessdoihave - can be used with | `whataccessdoihave` by users
New report - SearchHeadLevel - Dashboard load times
New report - SearchHeadLevel - Scheduled searches status
Updated dashboard - Troubleshooting Resource Usage Per User Drilldown - now uses `search_et/search_lt`
Removed report - What access do I have? (Replaced by macro/What access do I have without REST)

Upgraded Splunk python SDK to 1.6.6, note if this causes problems with other applications removing the bin directory only disables the "Search Queries summary non-exact match" report

### 2.4.5
Minor corrections

Updated SearchHeadLevel - Search Queries By Type Audit Logs - minor tweak to macroWithIndexClause
Updated SearchHeadLevel - Search Queries By Type Audit Logs macro version - minor tweak to macroWithIndexClause and hasMacro
Updated SearchHeadLevel - Search Queries By Type Audit Logs macro version other - minor tweak to macroWithIndexClause and hasMacro

### 2.4.4
New command - streamfilter
New command - streamfilterwildcard
New dashboard - Troubleshooting Resource Usage Per User
New dashboard - Troubleshooting Resource Usage Per User Drilldown
New report - SearchHeadLevel - Index access list by user
New report - SearchHeadLevel - Index list report
New report - SearchHeadLevel - Role access list by user
New report - SearchHeadLevel - Scheduled Search Efficiency
New report - SearchHeadLevel - Search Queries Per Day Audit Logs
New report - SearchHeadLevel - Search Queries By Type Audit Logs
New report - SearchHeadLevel - Search Queries By Type Audit Logs macro version
New report - SearchHeadLevel - Search Queries By Type Audit Logs macro version other
New report - SearchHeadLevel - Search Queries summary exact match
New report - SearchHeadLevel - Search Queries summary non-exact match
New report - SearchHeadLevel - Users with auto-finalized searches
New report - What Access Do I Have Without REST? To work without the `dispatch_rest_to_indexers`
Updated alert - AllSplunkEnterpriseLevel - Email Sending Failures - to make it easier to automate
Updated alert - SearchHeadLevel - Captain Switchover Occurring - to ignore a harmless warning message (NOT_LEADER)
Updated alert SearchHeadLevel - Scheduled Searches That Cannot Run to no longer ignore map alerts from this app
Updated alert - SearchHeadLevel - Scheduled searches not specifying an index macro version - to use an improved macro match
Updated alert - SearchHeadLevel - User - Dashboards searching all indexes macro version - to use an improved macro match
Updated dashboard Troubleshooting indexer CPU as sort was not working
Updated report - SearchHeadLevel - Macro report - to use `splunk_server=local`
Updated report - What Access Do I Have? to use `splunk_server=local`
Updated report - What Access Do I Have Without REST? to supply index list

### 2.4.3
A very minor release, the app inspect CLI and REST API provided different results on what needed to be fixed

Updated alert SearchHeadLevel - Users exceeding the disk quota introspection to not throw an error in the map command for no results
Updated alert SearchHeadLevel - Users exceeding the disk quota to not throw an error in the map command for no results

### 2.4.2
A very minor release, the app inspect badge does not allow external dependencies so changing 1 alert to get the badge

Updated alert SearchHeadLevel - Users exceeding the disk quota introspection to comment out sendresults command

### 2.4.1
Introduced an updated navigation menu to navigate around the alerts, reports and dashboards available in the app
Changed label of all dashboards to have Dashboard - ... this is just to make the navigation menu work as expected

New alert IndexerLevel - Buckets changes per day
New alert IndexerLevel - Timestamp parsing issues combined alert
New report SearchHeadLevel - Audit log search example only
Updated alert IndexerLevel - Future Dated Events that appeared in the last week to +10y instead of +20y
Updated alert IndexerLevel - Indexer Queues May Have Issues - to work with multiple pipelines
Updated alert IndexerLevel - Buckets rolling more frequently than expected with an improved regex
Updated alert SearchHeadLevel - Captain Switchover Occurring - to ignore manual captain transfers
Corrected alert SearchHeadLevel - Determine query scan density with a relevant query

Note 2.4.0 was never released

### 2.3.9
Updated alert SearchHeadLevel - Detect searches hitting corrupt buckets to detect 1 more variation of the issue
Updated alert SearchHeadLevel - Users exceeding the disk quota to include username
Updated alert SearchHeadLevel - Scheduled Searches That Cannot Run to ignore the new report (SearchHeadLevel - Users exceeding the disk quota introspection)
Updated report ForwarderLevel - Forwarders connecting to a single endpoint for extended periods (and UF level version) to use the hostname/name parameters
Renamed alert IndexerLevel - ERROR from linebreaker to IndexerLevel - Data parsing error
New report SearchHeadLevel - Users exceeding the disk quota introspection
New report SearchHeadLevel - Users exceeding the disk quota introspection cleanup

### 2.3.8
New reports for diagnosing forwarder issues, alerts around bucket corruption and peer connection failures
New dashboards for troubleshooting sourcetypes or buckets rolled per day
Updated all alerts with an investigationQuery to use `index=*` explicitly rather than assume the admin has all indexes listed in the indexes searched by default list

Update summary:
New alert - IndexerLevel - Detect bucket corruption
New alert - SearchHeadLevel - Indexer Peer Connection Failures
Updated alert ClusterMasterLevel - Per index status to 5 minute intervals for certification purposes
Renamed alert IndexerLevel - Detect bucket corruption to a report IndexerLevel - Report on bucket corruption (refer to IndexerLevel - Unclean Shutdown - Fsck for an alert)
New report - ForwarderLevel - Forwarders connecting to a single endpoint for extended periods
New report - ForwarderLevel - Forwarders connecting to a single endpoint for extended periods UF level
New report - SearchHeadLevel - Determine query scan density
New report - SearchHeadLevel - Detect searches hitting corrupt buckets
New dashboard - Issues per sourcetype, a combination of timestamp parsing, future based and past data searches to look at a single problematic sourcetype
New dashboard - Rolled buckets by index, a dashboard to assist with determing which index is rolling the most buckets

### 2.3.5
Update summary:
Updated IndexerLevel - Cold data location approaching size limits to handle only maxTotalDataSizeMB been set
Updated Future Dated Events that appeared in the last week to use +10y and 7.1 rejects +20y
Corrected AllSplunkEnterpriseLevel - TCP or SSL Config Issue to remove extra ( symbol
Corrected SearchHeadLevel - User - Dashboards searching all indexes macro version to refer to correct lookup name
Corrected dashboard for troubleshooting indexer CPU to handle standalone server
Inclusion of alternative app icons to work in 7.1

### 2.3.4
Update summary:
Updated SearchHeadLevel - Scheduled searches not specifying an index to exclude 1 additional type of search
Updated SearchHeadLevel - KVStore Or Conf Replication Issues Are Occurring to detect a disconnected member scenario
Updated Troubleshooting indexer CPU & drilldown dashboards to include commmas and the search head field (to make it easier to update to search head instead of indexer hosts)

### 2.3.3
Update summary:
New alert SearchHeadLevel - Disabled modular inputs are running
Updated SearchHeadLevel - Detect MongoDB errors to timechart to have no limit on the number of hosts involved
Updated the shutdown macros to find one additional scenarios

### 2.3.2
Due to resourcing issues on the search heads this includes a few warnings/errors related to performance issues

Update summary:
New alert AllSplunkEnterpriseLevel - Splunk Servers with resource starvation
New alert IndexerLevel - S2SFileReceiver Error
New alert SearchHeadLevel - Captain Switchover Occurring
Updated ForwarderLevel - Splunk Universal Forwarders that are time shifting to include "System time went backwards by..."
Updated IndexerLevel - Failures To Parse Timestamp Correctly (excluding breaking issues) to show when the failure related to been outside the acceptable time window
Updated SearchHeadLevel - User - Dashboards searching all indexes to simplify regex (ignore anything starting with a pipe symbol)
Updated SearchHeadLevel - User - Dashboards searching all indexes macro version to simplify regex (ignore anything starting with a pipe symbol)
Corrected AllSplunkEnterpriseLevel - sendmodalert errors to not show random `savedsearch_names` when no match is found
Corrected SearchHeadLevel - Alerts that have not fired an action in X days to only show alerts relevant to the current search head/cluster

### 2.3.1
Update summary:
New alert AllSplunkEnterpriseLevel - Non-existent roles are assigned to users
New alert IndexerLevel - Index not defined
New alert IndexerLevel - Search Failures
New alert SearchHeadLevel - Scheduled searches not specifying an index macro version (detect lack of index= with 1 level of macro expansion)
New alert SearchHeadLevel - Saved Searches with privileged owners and excessive write perms (detect 1 way of accessing data outside your level of access)
New alert SearchHeadLevel - User - Dashboards searching all indexes macro version
New report SearchHeadLevel - Macro report (required by "macro version" alerts)
Updated AllSplunkEnterpriseLevel - TCP or SSL Config Issue to include an additional scenario as reported by a customer
Updated SearchHeadLevel - Scheduled searches not specifying an index to not find searches with macros and to include example query
Updated SearchHeadLevel - Scheduled Searches That Cannot Run to make the message field accurate in all situations
Updated SearchHeadLevel - User - Dashboards searching all indexes to include example query to find indexes, and to not find macro-based queries
Corrected AllSplunkLevel - Unable To Distribute to Peer
Corrected IndexerLevel - Failures To Parse Timestamp Correctly (excluding breaking issues) to correctly exclude broken events & to handle newer 7.0.2 errors

### 2.3.0
Minor updates to a few alerts and a new alert

Update summary:
New alert AllSplunkEnterpriseLevel - Detect LDAP groups that no longer exist
New alert ClusterMasterLevel - Per index status
New report ClusterMasterLevel - Primary bucket count per peer
Updated AllSplunkEnterpriseLevel - TCP or SSL Config Issue to find most recent (not oldest example)
Updated AllSplunkEnterpriseLevel - Splunk Scheduler skipped searches and the reason to exclude the timewindow upto 10 minutes post-shutdown of an indexer
Updated AllSplunkLevel - TCP Output Processor has paused the data flow to use a stats command instead of raw/host information
Updated DeploymentServer - Unsupported attribute within DS config - to find most recent (not oldest example)
Updated IndexerLevel - Failures To Parse Timestamp Correctly (excluding breaking issues) - to find most recent (not oldest example)
Updated SearchHeadLevel - Detect MongoDB errors - mild tweak to output data, added customisation macros
Updated SearchHeadLevel - Scheduled Searches That Cannot Run - to detect errors in splunkd related to saved searches
Corrected SearchHeadLevel - User - Dashboards searching all indexes - a newline resulted in it working in search but not via the scheduler!

### 2.2
Not released, combined with 2.3.0
Attempt to reduce false alarms and improve investigationQuery searches
Created macros for shutdown events for indexers/search heads/enterprise servers for excluding false alarms related to restarts

Update summary:
New macro `splunkadmins_shutdown_list`
New macro `splunkadmins_shutdown_time`
Updated AllSplunkEnterpriseLevel - Splunk Scheduler skipped searches and the reason - to use shutdown macro
Updated AllSplunkEnterpriseLevel - Splunk Scheduler excessive delays in executing search - to use shutdown macro
Updated AllSplunkLevel - TCP Output Processor has paused the data flow - to use shutdown macro
Updated AllSplunkLevel - Unable To Distribute to Peer - to use shutdown macro
Updated ForwarderLevel - Splunk forwarders are having issues with sending data to indexers - to use shutdown macro
Updated ForwarderLevel - SplunkStream Errors - to use shutdown macro
Updated ForwarderLevel - Unusual number of duplication alerts - to use shutdown macro & changed the alert to fire on >10 results per host
Updated IndexerLevel - Weekly Truncated Logs Report - hostnames wildcarded to deal with short names (for syslog for example)
Updated SearchHeadLevel - Detect MongoDB errors - timespan increased to 10 minutes and 5 minutes produces false alarms, and added shutdown macro
Updated SearchHeadLevel - KVStore Or Conf Replication Issues Are Occurring - to use shutdown macro

### 2.1
Added macros which can be customised to the majority of alerts, this reduces the need to customise the alert itself and should make upgrading to new versions of the application easier...

Update summary:
New alert AllSplunkEnterpriseLevel - Unable to dispatch searches due to disk space
New alert IndexerLevel - Unclean Shutdown - Fsck
New macros - various macros introduced due to customer feedback about the requirement to customise the alerts
Updated SearchHeadLevel - Users exceeding the disk quota to list top 10 consumers of disk
Updated SearchHeadLevel - Scheduled Searches That Cannot Run (to ignore the above)
Updated IndexerLevel - Failures To Parse Timestamp Correctly (excluding breaking issues) to list sources per sourcetype/host
Updated ForwarderLevel - Splunk Insufficient Permissions to Read Files to include new macro, hint, invesQuery & to improve the accuracy
Updated SearchHeadLevel - Detect MongoDB errors (customer feedback, includes F/fatal errors now)
README and description updates for searches

### 2.0
Multiple searches now have an "investigationQuery" in them, the idea is that you can copy and paste the output into a search window and see results relevant to the particular alert
The last few releases have been attempting to reduce false alarms from alerts related to server restarts

Update summary:
New alert IndexerLevel - Cold data location approaching size limits
New/renamed alert AllSplunkEnterpriseLevel - Splunk Scheduler excessive delays in executing search
New/renamed alert AllSplunkEnterpriseLevel - Splunk Scheduler skipped searches and the reason
Updated AllSplunkLevel - Time skew on Splunk Servers
Updated IndexerLevel - Future Dated Events that appeared in the last week
Updated IndexerLevel - Time format has changed multiple log types in one sourcetype
Updated IndexerLevel - Failures To Parse Timestamp Correctly (excluding breaking issues)
Updated IndexerLevel - Weekly Broken Events Report
Updated IndexerLevel - Weekly Truncated Logs Report
Updated IndexerLevel - Old data appearing in Splunk indexes
Updated IndexerLevel - Valid Timestamp Invalid Parsed Time
Updated IndexerLevel - Too many events with the same timestamp
Updated IndexerLevel - Large multiline events using `SHOULD_LINEMERGE` setting
Updated SearchHeadLevel - Users exceeding the disk quota
Updated IndexerLevel - Indexer Queues May Have Issues (to be less sensitive to indexqueue issues)
Corrected AllSplunkLevel - TCP Output Processor has paused the data flow
Corrected ForwarderLevel - Splunk Universal Forwarders that are time shifting
Removed AllSplunkEnterpriseLevel - Splunk Servers with time skew (replaced by Time skew on Splunk Servers)
Removed SearchHead Level - Splunk Scheduler excessive delays in executing search (renamed)
Removed SearchHeadLevel - Splunk Scheduler Skipped Searches and the reason (renamed)

### 1.9
New macro `splunkadmins_mongo_source`
New alert IndexerLevel - Too many events with the same timestamp
New alert SearchHeadLevel - Detect MongoDB errors
New dashboard Data Model Status
New dashboard Data Model Rebuild Monitor
Updated AllSplunkEnterpriseLevel - Email Sending Failures to include to the toaddress
Updated SearchHeadLevel - Splunk Users Violating the Search Quota to detect an alternative log message
Updated Scheduled searches not specifying an index
Updated SearchHeadLevel - Scheduled Searches without a configured earliest and latest time
Updated ForwarderLevel - File Too Small to checkCRC occurring multiple times, to handle spaces in filename
Updated ForwarderLevel - crcSalt or initCrcLength change may be required
Updated IndexerLevel - Indexer Queues May Have Issues to be less sensitive
Updated IndexerLevel - Splunk Indexers Losing Contact With Master for an additional scenario
Updated AllSplunkEnterpriseLevel - ulimit on Splunk enterprise servers is below 8192 to improve emails
Corrected AllSplunkLevel - Splunk forwarders that are not talking to the deployment server

### 1.8
New alert IndexerLevel - Peer will not return results due to outdated generation
New alert SearchHeadLevel - Scheduled searches failing in cluster with 404 error
Updated ForwarderLevel - File Too Small to checkCRC occurring multiple times to have the correct dispatch application
Updated AllSplunkEnterpriseLevel - Email Sending Failures with saved search name
Updated IndexerLevel - Indexer replication queue issues to some peers to be less sensitive as this cannot be tuned in 7.0.0
Updated AllSplunkLevel - Unable To Distribute to Peer to include the peer name
Updated IndexerLevel - Indexer Queues May Have Issues to ensure it fires when neccesary but is not too noisy (this may require tuning)
Corrected ForwarderLevel - Bandwidth Throttling Occurring, this alert was not working as expected

### 1.7
New macro `splunkadmins_splunkuf_source`
New alert "AllSplunkEnterpriseLevel - TCP or SSL Config Issue" for detecting when the listener ports fail to start on a HF/Indexer
Updated macro splunkindexerhostsvalue to include `splunk_server=`
Updated searches to use (`splunkadmins_splunkd_source`) in brackets so it looks valid when expanded (and allows a future OR/NOT statement to be added before or after with no unexpected side effects)
Updated a few comments and improved some searches to narrow down the required hosts/sources/sourcetypes
Removed unused macro splunkenterprisehostsvalue
Removed hardcoded references to the location of splunkd.log file and replaced with `splunkadmins_splunkd_source` macro
Removed a few unnessary fields/fixed some other minor issues within the file

### 1.6
Removed "Splunk Alert failures" and updated "AllSplunkEnterpriseLevel - sendmodalert errors", also updated "Time format has changed" alert to have more clear output via email

### 1.5
Updated Splunk Alert Failures alert and the Time format has changed alerts to have more clear output via email
Simplified "Scheduled Searches without a configured earliest and latest time", and "Scheduled searches not specifying an index"

### 1.4
Two new alerts LicenseMaster - Duplicated License Situation, DeploymentServer - Unsupported attribute within DS config
Simplified Scheduled Searches without a configured earliest and latest time, and Scheduled searches not specifying an index
Created a macro `splunkadmins_splunkd_source` for Windows users or others using non-standard Splunk installation directories

### 1.0 to 1.3
Creation of app, addition of icons and removal of email functionality from the app for Splunk certification purposes

## Other
Icons made by [Freepik](http://www.freepik.com) from www.flaticon.com is licensed by [Creative Commons BY 3.0](http://creativecommons.org/licenses/by/3.0)

### Misc testing notes for SearchHeadLevel - Detect changes to knowledge objects
calcfields:
/data/props/calcfields
/servicesNS/admin/search/data/props/calcfields (GUI goes via /manager/ first)
/services/data/props/calcfield
https://localhost:8089/servicesNS/nobody/search/configs/conf-props?count=0 <-- did not work/no data found

Saved searches:
/servicesNS/nobody/search/configs/conf-savedsearche
/services/configs/conf-savedsearches
/services/saved/searches
/services/admin/savedsearch
/en-US/splunkd/__raw/servicesNS/admin/search/saved/searches/

dashboards:
/services/data/ui/views
/en-US/splunkd/__raw/servicesNS/admin/search/data/ui/views
/services/admin/views/

fieldaliases:
/servicesNS/admin/search/data/props/fieldaliases (GUI goes via /manager/ first)
/servicesNS/admin/search/data/props//fieldaliases
/services/admin//fieldaliases
/services/configs/conf-props

field extractions:
/servicesNS/admin/search/data/props/extractions
/services/admin/props-extract
/services/configs/conf-props

fieldtransforms:
/servicesNS/admin/search/data/transforms/extractions
/services/admin//transforms-extract
/services/configs/conf-transforms

workflowactions:
/data/ui/workflow-actions
/services/admin//workflow-actions/TestWorkflow
/services/configs/conf-workflow_actions

sourcetype renaming:
/data/props/sourcetype-rename
/admin//sourcetype-rename
/services/configs/conf-props

tags:
/configs/conf-tags
/admin/tags
/saved/ntags
/saved/fvtags

eventtypes:
/saved/eventtypes
/admin//eventtypes
/configs/conf-eventtypes

navMenu:
/data/ui/nav
/admin/nav/

datamodel:
/datamodel/model
/configs/conf-datamodels
/admin//datamodeledit
/admin//datamodel-files

kvstore:
/storage/collections/config
/configs/conf-collections
/admin//collections-conf

/configs/conf-viewstates
Skipped

times:
/data/ui/times
/configs/conf-times
/admin//conf-times

UI panels:
/data/ui/panels
/configs/conf-panels

automatic lookups:
/data/transforms/lookups
/admin//transforms-lookup
/services/configs/conf-transforms

lookup definitions:
/data/props/lookups
/admin//props-lookup
/services/configs/conf-props

macros:
/configs/conf-macros
/data/macros
/admin/macros
