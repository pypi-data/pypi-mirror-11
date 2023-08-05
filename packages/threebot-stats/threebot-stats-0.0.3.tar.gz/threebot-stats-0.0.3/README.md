# 3bot-stats

> Statistics and Performance monitoring for [3bot](https://github.com/3bot/3bot).

## Quickstart

Install 3bot-stats::

    pip install 3bot-stats -i http://********pypi.arteria.ch/pypi  --extra-index-url=http://pypi.python.org/simple

Then use it in a project::

    import threebot_stats


## Planned Features

* avg response time per workflow
* number of logs per workflow
* impact = avg response time * number of logs per workflow
* simple graph for latest n logs / [example](http://2.bp.blogspot.com/_3rU41dez5TI/TIz-i8WFnTI/AAAAAAAAAYE/pnVJa_r9iVw/s320/gets_by_pk_-_response_time_-_average_%2526_98th_percentile_-_16_core_server.png)
* EXTRA: graph for all workflows and their response times (to identify time-consuming workflows) / [example](http://www.albemarle.org/upload/images/Pictures/Departments/Performance_Management/pictures/2012%20Q4/Police-Response%20Rural.png)
