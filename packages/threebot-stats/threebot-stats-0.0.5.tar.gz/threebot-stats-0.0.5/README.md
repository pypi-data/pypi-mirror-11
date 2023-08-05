# 3bot-stats

> Statistics and Performance monitoring for [3bot](https://github.com/3bot/3bot).

## Quickstart

Install 3bot-stats::

    pip install 3bot-stats -i http://********pypi.arteria.ch/pypi  --extra-index-url=http://pypi.python.org/simple

Then use it in a project::

    import threebot_stats

## Usage

Workflow statistics are available at `/stats/<slug>`, where `slug` is the primary key visible in the Workflow's URL.

For every Workflow, the average response time for all completed logs, the number of logs since creation, and the totalled execution time ("impact") are listed. A chart visualizes the response times of the last 10 logs.

## Planned Features

* A graph for all workflows and their response times (to identify time-consuming workflows) / [example](http://www.albemarle.org/upload/images/Pictures/Departments/Performance_Management/pictures/2012%20Q4/Police-Response%20Rural.png)
