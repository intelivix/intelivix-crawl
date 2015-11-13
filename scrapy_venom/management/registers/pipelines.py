# -*- coding: utf-8 -*-

from scrapy_venom.management.registers import utils


__all__ = ['register_pipelines']


def generate_path(project_name, pipeline):
    app, pipeline_name = pipeline.split('.')
    return '{}.spiders.{}.pipelines.{}'.format(
        project_name, app, pipeline_name)


def register_pipelines(pipelines):
    project_name = utils.get_project_name()
    item_pipelines = {}
    for pipeline, priority in pipelines.iteritems():
        pipeline_path = generate_path(project_name, pipeline)
        item_pipelines[pipeline_path] = priority
    return item_pipelines
