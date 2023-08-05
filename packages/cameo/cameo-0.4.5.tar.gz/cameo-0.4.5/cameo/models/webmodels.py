# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
WebModels API
-------------

A high level API for retrieving models from the
http://darwin.di.uminho.pt/models and http://bigg.ucsd.edu databases
"""

from __future__ import absolute_import, print_function
from cameo.util import str_to_valid_variable_name

__all__ = ['index_models_minho', 'index_models_bigg', 'bigg', 'minho']

import io
import tempfile
import json

import requests
from pandas import DataFrame

from cobra.io import load_json_model, read_sbml_model

from cameo import util
from cameo.core.solver_based_model import to_solver_based_model

import logging
logger = logging.getLogger(__name__)


class NotFoundException(Exception):
    def __init__(self, type, index, *args, **kwargs):
        message = "Could not retrieve %s for entry with index %i" % (type, index)
        Exception.__init__(self, message, *args, **kwargs)


class ModelFacadeBigg(util.ModelFacade):

    def _load_model(self):
        return get_model_from_bigg(self._id)


class ModelFacadeMinho(util.ModelFacade):

    def _load_model(self):
        return get_model_from_uminho(self._id)


def index_models_minho(host="http://darwin.di.uminho.pt/models"):
    """
    Retrieves a summary of all models in the database.

    Parameters
    ----------
    host: the service host (optional, default: http://darwin.di.uminho.pt/models)

    Returns
    -------
    pandas.DataFrame
        summary of the models in the database
    """
    uri = host + "/models.json"
    try:
        response = requests.get(uri)
    except requests.ConnectionError as e:
        logger.error("Cannot reach %s. Are you sure that you are connected to the internet?" % host)
        raise e
    if response.ok:
        response = json.loads(response.text)
        return DataFrame(response, columns=["id", "name", "doi", "author", "year", "formats", "organism", "taxonomy"])
    else:
        raise Exception("Could not index available models. %s returned status code %d" % (host, response.status_code))


def get_model_from_uminho(index, host="http://darwin.di.uminho.pt/models"):
    sbml_file = get_sbml_file(index, host)
    sbml_file.close()
    return to_solver_based_model(read_sbml_model(sbml_file.name))


def get_sbml_file(index, host="http://darwin.di.uminho.pt/models"):
    temp = tempfile.NamedTemporaryFile()
    temp.delete = False
    uri = host + "/models/%i.sbml" % index
    try:
        response = requests.get(uri)
    except requests.ConnectionError as e:
        logger.error("Cannot reach {}. Are you sure that you are connected to the internet?".format(host))
        raise e
    if response.ok:

        temp.write(response.text.encode('utf-8'))
        temp.flush()
        return temp
    else:
        raise NotFoundException("sbml", index)

def index_models_bigg():
    try:
        response = requests.get('http://bigg.ucsd.edu/api/v2/models')
    except requests.ConnectionError as e:
        logger.error("Cannot reach http://bigg.ucsd.edu. Are you sure that you are connected to the internet?")
        raise e
    if response.ok:
        return DataFrame.from_dict(response.json()['results'])
    else:
        raise Exception("Could not index available models. bigg.ucsd.edu returned status code {}".format(response.status_code))

def get_model_from_bigg(id):
    try:
        response = requests.get('http://bigg.ucsd.edu/api/v2/models/{}/download'.format(id))
    except requests.ConnectionError as e:
        logger.error("Cannot reach http://bigg.ucsd.edu. Are you sure that you are connected to the internet?")
        raise e
    if response.ok:
        with io.StringIO(response.text) as f:
            return to_solver_based_model(load_json_model(f))
    else:
        raise Exception("Could not download model {}. bigg.ucsd.edu returned status code {}".format(id, response.status_code))

class ModelDB(object): pass

bigg = ModelDB()
try:
    model_ids = index_models_bigg().bigg_id
except requests.ConnectionError:
    pass
else:
    for id in model_ids:
        setattr(bigg, str_to_valid_variable_name(id), ModelFacadeBigg(id))

minho = ModelDB()
try:
    minho_models = index_models_minho()
    model_indices = minho_models.id
    model_ids = minho_models.name
except requests.ConnectionError:
    pass
else:
    for index, id in zip(model_indices, model_ids):
        setattr(minho, str_to_valid_variable_name(id), ModelFacadeMinho(index))


if __name__ == "__main__":
    print(index_models_minho())
    from cameo import load_model
    model = load_model(get_sbml_file(2))
    print(model.objective)
