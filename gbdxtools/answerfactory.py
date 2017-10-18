"""
AnswerFactory Project and Recipe interfaces

Contact: nricklin@digitalglobe.com
Contact: mtrotter@digitalglobe.com
"""
from __future__ import absolute_import
from builtins import object

import requests
import json
import datetime

from gbdxtools.auth import Auth

class Recipe(object):
    def __init__(self, **kwargs):
        '''
        Construct an instance of an AnswerFactory Recipe

        Args:
            **kwargs

        Returns:
            An instance of a Recipe.

        '''
        interface = Auth(**kwargs)
        self.base_url = '%s/answer-factory-recipe-service/api/recipe'
        self.gbdx_connection = interface.gbdx_connection
        self.logger = interface.logger

    def get(self, recipe_id):
        '''
        Retrieves an AnswerFactory Recipe by id

        Args:
            recipe_id The id of the recipe

        Returns:
            A JSON representation of the recipe
        '''
        self.logger.debug('Retrieving recipe by id: ' + recipe_id)
        url = '%(base_url)s/%(recipe_id)s' % {
            'base_url': self.base_url, 'recipe_id': recipe_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()

    def save(self, recipe):
        '''
        Saves an AnswerFactory Recipe

        Args:
            recipe (dict): Dictionary specifying a recipe

        Returns:
            AnswerFactory Recipe id
        '''
        # test if this is a create vs. an update
        if 'id' in recipe:
            # update -> use put op
            self.logger.debug("Updating existing recipe: " + json.dumps(recipe))
            url = '%(base_url)s/%(recipe_id)s' % {
                'base_url': self.base_url, 'recipe_id': recipe['id']
            }
            r = self.gbdx_connection.put(url, recipe)
            r.raise_for_status()
            return recipe['id']
        else:
            # create -> use post op
            self.logger.debug("Creating new recipe: " + json.dumps(recipe))
            url = self.base_url
            r = self.gbdx_connection.post(url, recipe)
            r.raise_for_status()
            recipe_json = r.json()
            return recipe_json['id']

    def delete(self, recipe_id):
        '''
        Deletes an AnswerFactory Recipe by id

        Args:
             recipe_id: The id of the recipe to delete

        Returns:
             Nothing
        '''
        self.logger.debug('Deleting recipe by id: ' + recipe_id)
        url = '%(base_url)s/%(recipe_id)s' % {
            'base_url': self.base_url, 'recipe_id': recipe_id
        }
        r = self.gbdx_connection.delete(url)
        r.raise_for_status()



class Project(object):
    def __init__(self, **kwargs):
        '''
        Construct an instance of an AnswerFactory Project

        Args:
            **kwargs

        Returns:
            An instance of a Project.

        '''
        interface = Auth(**kwargs)
        self.base_url = '%s/answer-factory-project-service/api/project'
        self.gbdx_connection = interface.gbdx_connection
        self.logger = interface.logger

    def get(self, project_id):
        '''
        Retrieves an AnswerFactory Project by id

        Args:
            project_id

        Returns:
            A JSON representation of the project
        '''
        self.logger.debug('Retrieving project by id: ' + project_id)
        url = '%(base_url)s/%(project_id)s' % {
            'base_url': self.base_url, 'project_id': project_id
        }
        r = self.gbdx_connection.get(url)
        r.raise_for_status()
        return r.json()

    def save(self, project):
        '''
        Saves an AnswerFactory Project

        Args:
            project (dict): Dictionary specifying an AnswerFactory Project.

        Returns:
            AnswerFactory Project id
        '''

        # test if this is a create vs. an update
        if 'id' in project:
            # update -> use put op
            self.logger.debug('Updating existing project: ' + json.dumps(project))
            url = '%(base_url)s/%(project_id)s' % {
                'base_url': self.base_url, 'project_id': project['id']
            }
            r = self.gbdx_connection.put(url, project)
            r.raise_for_status()
            # updates only get the Accepted response -> return the original project id
            return project['id']
        else:
            self.logger.debug('Creating new project: ' + json.dumps(project))
            # create -> use post op
            url = self.base_url
            r = self.gbdx_connection.post(url, project)
            r.raise_for_status()
            project_json = r.json()
            # create returns the saved project -> return the project id that's saved
            return project_json['id']

    def delete(self, project_id):
        '''
        Deletes a project by id

        Args:
             project_id: The project id to delete

        Returns:
             Nothing
        '''
        self.logger.debug('Deleting project by id: ' + project_id)
        url = '%(base_url)s/%(project_id)s' % {
            'base_url': self.base_url, 'project_id': project_id
        }
        r = self.gbdx_connection.delete(url)
        r.raise_for_status()
