from enum import Enum
import numpy as np
import random

class Attitude(Enum):
    NEUTRAL  = (0.5, 0.05)
    POSITIVE = (0.75, 0.1)
    NEGATIVE = (0.25, 0.1)

class NormalDistribution:
    def __init__(self, attitude : Attitude):
        self.mean = attitude.value[0]
        self.std_deviation = attitude.value[1]

    def generateNumber(self):
        val = np.random.normal(loc=self.mean, scale=self.std_deviation)

        val = val * 2 - 1 #value has to be changed to [-1,1]
        if val > 1:
            return 1
        elif val < -1:
            return -1
        else:
            return val

class UniformDistribution:
    def __init__(self, min_val=-1, max_val=1):
        self.min_val = min_val
        self.max_val = max_val

    def generateNumber(self):
        val =  random.uniform(self.min_val, self.max_val)
        return val

TYPE_RANDOM = {
    "name": "random",
    # local trees (3c0b0b79-2b8c-4df9-95b9-4505443b3638)
    "62bcc15f-5f39-4239-963a-455498c34f79": UniformDistribution(), #Low
    "066372f5-9b21-46a3-a62a-76be0afd8f4e": UniformDistribution(), #Medium
    "2e94ef17-7ea1-42e0-b070-bba3a8debfd8": UniformDistribution(), #High

    # climate resilient trees (290951c4-ed76-4d5c-8d26-0ecc8ca42e59)
    "1a02a295-5afd-427a-bf1e-2b8065687380": UniformDistribution(), #Low
    "6f3a5204-1276-40f9-84dc-c8e139e5402d": UniformDistribution(), #Medium
    "5bd172ba-0076-456e-9ee2-0b81780a5da0": UniformDistribution(), #High

    # usable trees (5fee0b16-9ba2-4162-a98b-5c6170ab200e)
    "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8": UniformDistribution(), #Low
    "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1": UniformDistribution(), #Medium
    "3fb4ae3d-c892-4025-815f-6b6074ac3d3c": UniformDistribution(), #High

    # harvesting effort (8c7bd4d7-b91e-4518-99d4-7564df1d4207)
    "a755ba0d-fb8d-475a-a0f9-5ca267fd479f": UniformDistribution(), # Manual
    "653b4832-6647-426d-a18e-ee444ba67979": UniformDistribution(), # Harvester
    "dcb34d08-06f2-4426-a3a9-039cec1e6f6d": UniformDistribution(), # Self-driving Harvester

    # harvesting amount (c5b446ce-455a-44b5-b8be-178eef2848c2)
    "9e70ea9a-1311-48db-9238-cbc98da1ed2b": UniformDistribution(), #No harvest
    "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c": UniformDistribution(), #Low harvest
    "09594573-6fc5-4c62-9d5c-84b4ccf817a1": UniformDistribution(), #High harvest

    # wood price (3a375746-288f-4147-8065-9f6966389772)
    "8d2f5efe-db35-4b4d-9591-cf797335e3ba": UniformDistribution(), #Low
    "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93": UniformDistribution(), #Medium
    "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853": UniformDistribution(), #High   

    # public accessability (5d8ab41c-02bd-4478-9106-64e80bdb9728)
    "d59c52cf-0eb1-4ad9-9228-c5100c2b6237": UniformDistribution(), #Almost none
    "311389a2-c4b7-4a13-bf5a-04a1befad0e9": UniformDistribution(), #Low intensity
    "f08b7cd1-c470-4d6e-951d-a69a02b04849": UniformDistribution(), #High intensity
}

TYPE_ATHLETE = {
    "name": "athlete",
    # local trees (3c0b0b79-2b8c-4df9-95b9-4505443b3638)
    "62bcc15f-5f39-4239-963a-455498c34f79": NormalDistribution(Attitude.NEGATIVE), #Low
    "066372f5-9b21-46a3-a62a-76be0afd8f4e": NormalDistribution(Attitude.POSITIVE), #Medium
    "2e94ef17-7ea1-42e0-b070-bba3a8debfd8": NormalDistribution(Attitude.POSITIVE), #High

    # climate resilient trees (290951c4-ed76-4d5c-8d26-0ecc8ca42e59)
    "1a02a295-5afd-427a-bf1e-2b8065687380": NormalDistribution(Attitude.NEUTRAL), #Low
    "6f3a5204-1276-40f9-84dc-c8e139e5402d": NormalDistribution(Attitude.POSITIVE), #Medium
    "5bd172ba-0076-456e-9ee2-0b81780a5da0": NormalDistribution(Attitude.POSITIVE), #High

    # usable trees (5fee0b16-9ba2-4162-a98b-5c6170ab200e)
    "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8": NormalDistribution(Attitude.NEUTRAL), #Low
    "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1": NormalDistribution(Attitude.NEUTRAL), #Medium
    "3fb4ae3d-c892-4025-815f-6b6074ac3d3c": NormalDistribution(Attitude.NEGATIVE), #High

    # harvesting effort (8c7bd4d7-b91e-4518-99d4-7564df1d4207)
    "a755ba0d-fb8d-475a-a0f9-5ca267fd479f": NormalDistribution(Attitude.NEUTRAL), # Manual
    "653b4832-6647-426d-a18e-ee444ba67979": NormalDistribution(Attitude.NEGATIVE), # Harvester
    "dcb34d08-06f2-4426-a3a9-039cec1e6f6d": NormalDistribution(Attitude.NEGATIVE), # Self-driving Harvester

    # harvesting amount (c5b446ce-455a-44b5-b8be-178eef2848c2)
    "9e70ea9a-1311-48db-9238-cbc98da1ed2b": NormalDistribution(Attitude.POSITIVE), #No harvest
    "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c": NormalDistribution(Attitude.NEUTRAL), #Low harvest
    "09594573-6fc5-4c62-9d5c-84b4ccf817a1": NormalDistribution(Attitude.NEGATIVE), #High harvest

    # wood price (3a375746-288f-4147-8065-9f6966389772)
    "8d2f5efe-db35-4b4d-9591-cf797335e3ba": NormalDistribution(Attitude.NEUTRAL), #Low
    "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93": NormalDistribution(Attitude.NEUTRAL), #Medium
    "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853": NormalDistribution(Attitude.NEUTRAL), #High   

    # public accessability (5d8ab41c-02bd-4478-9106-64e80bdb9728)
    "d59c52cf-0eb1-4ad9-9228-c5100c2b6237": NormalDistribution(Attitude.NEGATIVE), #Almost none
    "311389a2-c4b7-4a13-bf5a-04a1befad0e9": NormalDistribution(Attitude.NEUTRAL), #Low intensity
    "f08b7cd1-c470-4d6e-951d-a69a02b04849": NormalDistribution(Attitude.POSITIVE), #High intensity
}

TYPE_OWNER = {
    "name": "owner",
    # local trees (3c0b0b79-2b8c-4df9-95b9-4505443b3638)
    "62bcc15f-5f39-4239-963a-455498c34f79": NormalDistribution(Attitude.POSITIVE), #Low
    "066372f5-9b21-46a3-a62a-76be0afd8f4e": NormalDistribution(Attitude.NEUTRAL), #Medium
    "2e94ef17-7ea1-42e0-b070-bba3a8debfd8": NormalDistribution(Attitude.NEGATIVE), #High

    # climate resilient trees (290951c4-ed76-4d5c-8d26-0ecc8ca42e59)
    "1a02a295-5afd-427a-bf1e-2b8065687380": NormalDistribution(Attitude.POSITIVE), #Low
    "6f3a5204-1276-40f9-84dc-c8e139e5402d": NormalDistribution(Attitude.NEUTRAL), #Medium
    "5bd172ba-0076-456e-9ee2-0b81780a5da0": NormalDistribution(Attitude.NEGATIVE), #High

    # usable trees (5fee0b16-9ba2-4162-a98b-5c6170ab200e)
    "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8": NormalDistribution(Attitude.NEUTRAL), #Low
    "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1": NormalDistribution(Attitude.NEUTRAL), #Medium
    "3fb4ae3d-c892-4025-815f-6b6074ac3d3c": NormalDistribution(Attitude.POSITIVE), #High

    # harvesting effort (8c7bd4d7-b91e-4518-99d4-7564df1d4207)
    "a755ba0d-fb8d-475a-a0f9-5ca267fd479f": NormalDistribution(Attitude.NEUTRAL), # Manual
    "653b4832-6647-426d-a18e-ee444ba67979": NormalDistribution(Attitude.POSITIVE), # Harvester
    "dcb34d08-06f2-4426-a3a9-039cec1e6f6d": NormalDistribution(Attitude.POSITIVE), # Self-driving Harvester

    # harvesting amount (c5b446ce-455a-44b5-b8be-178eef2848c2)
    "9e70ea9a-1311-48db-9238-cbc98da1ed2b": NormalDistribution(Attitude.NEGATIVE), #No harvest
    "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c": NormalDistribution(Attitude.POSITIVE), #Low harvest
    "09594573-6fc5-4c62-9d5c-84b4ccf817a1": NormalDistribution(Attitude.POSITIVE), #High harvest

    # wood price (3a375746-288f-4147-8065-9f6966389772)
    "8d2f5efe-db35-4b4d-9591-cf797335e3ba": NormalDistribution(Attitude.NEUTRAL), #Low
    "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93": NormalDistribution(Attitude.POSITIVE), #Medium
    "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853": NormalDistribution(Attitude.POSITIVE), #High   

    # public accessability (5d8ab41c-02bd-4478-9106-64e80bdb9728)
    "d59c52cf-0eb1-4ad9-9228-c5100c2b6237": NormalDistribution(Attitude.POSITIVE), #Almost none
    "311389a2-c4b7-4a13-bf5a-04a1befad0e9": NormalDistribution(Attitude.NEUTRAL), #Low intensity
    "f08b7cd1-c470-4d6e-951d-a69a02b04849": NormalDistribution(Attitude.NEGATIVE), #High intensity
}

TYPE_ENVIRONMENTALIST = {
    "name": "environmentalist",
    # local trees (3c0b0b79-2b8c-4df9-95b9-4505443b3638)
    "62bcc15f-5f39-4239-963a-455498c34f79": NormalDistribution(Attitude.NEGATIVE), #Low
    "066372f5-9b21-46a3-a62a-76be0afd8f4e": NormalDistribution(Attitude.NEGATIVE), #Medium
    "2e94ef17-7ea1-42e0-b070-bba3a8debfd8": NormalDistribution(Attitude.POSITIVE), #High

    # climate resilient trees (290951c4-ed76-4d5c-8d26-0ecc8ca42e59)
    "1a02a295-5afd-427a-bf1e-2b8065687380": NormalDistribution(Attitude.NEUTRAL), #Low
    "6f3a5204-1276-40f9-84dc-c8e139e5402d": NormalDistribution(Attitude.NEUTRAL), #Medium
    "5bd172ba-0076-456e-9ee2-0b81780a5da0": NormalDistribution(Attitude.NEGATIVE), #High

    # usable trees (5fee0b16-9ba2-4162-a98b-5c6170ab200e)
    "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8": NormalDistribution(Attitude.NEUTRAL), #Low
    "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1": NormalDistribution(Attitude.NEGATIVE), #Medium
    "3fb4ae3d-c892-4025-815f-6b6074ac3d3c": NormalDistribution(Attitude.NEGATIVE), #High

    # harvesting effort (8c7bd4d7-b91e-4518-99d4-7564df1d4207)
    "a755ba0d-fb8d-475a-a0f9-5ca267fd479f": NormalDistribution(Attitude.POSITIVE), # Manual
    "653b4832-6647-426d-a18e-ee444ba67979": NormalDistribution(Attitude.NEGATIVE), # Harvester
    "dcb34d08-06f2-4426-a3a9-039cec1e6f6d": NormalDistribution(Attitude.NEGATIVE), # Self-driving Harvester

    # harvesting amount (c5b446ce-455a-44b5-b8be-178eef2848c2)
    "9e70ea9a-1311-48db-9238-cbc98da1ed2b": NormalDistribution(Attitude.POSITIVE), #No harvest
    "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c": NormalDistribution(Attitude.NEUTRAL), #Low harvest
    "09594573-6fc5-4c62-9d5c-84b4ccf817a1": NormalDistribution(Attitude.NEGATIVE), #High harvest

    # wood price (3a375746-288f-4147-8065-9f6966389772)
    "8d2f5efe-db35-4b4d-9591-cf797335e3ba": NormalDistribution(Attitude.NEUTRAL), #Low
    "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93": NormalDistribution(Attitude.NEUTRAL), #Medium
    "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853": NormalDistribution(Attitude.NEUTRAL), #High   

    # public accessability (5d8ab41c-02bd-4478-9106-64e80bdb9728)
    "d59c52cf-0eb1-4ad9-9228-c5100c2b6237": NormalDistribution(Attitude.POSITIVE), #Almost none
    "311389a2-c4b7-4a13-bf5a-04a1befad0e9": NormalDistribution(Attitude.NEUTRAL), #Low intensity
    "f08b7cd1-c470-4d6e-951d-a69a02b04849": NormalDistribution(Attitude.NEGATIVE), #High intensity
}

TYPE_CONSUMER = {
    "name": "consumer",
    # local trees (3c0b0b79-2b8c-4df9-95b9-4505443b3638)
    "62bcc15f-5f39-4239-963a-455498c34f79": NormalDistribution(Attitude.NEUTRAL), #Low
    "066372f5-9b21-46a3-a62a-76be0afd8f4e": NormalDistribution(Attitude.NEUTRAL), #Medium
    "2e94ef17-7ea1-42e0-b070-bba3a8debfd8": NormalDistribution(Attitude.NEGATIVE), #High

    # climate resilient trees (290951c4-ed76-4d5c-8d26-0ecc8ca42e59)
    "1a02a295-5afd-427a-bf1e-2b8065687380": NormalDistribution(Attitude.NEUTRAL), #Low
    "6f3a5204-1276-40f9-84dc-c8e139e5402d": NormalDistribution(Attitude.NEUTRAL), #Medium
    "5bd172ba-0076-456e-9ee2-0b81780a5da0": NormalDistribution(Attitude.NEGATIVE), #High

    # usable trees (5fee0b16-9ba2-4162-a98b-5c6170ab200e)
    "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8": NormalDistribution(Attitude.NEGATIVE), #Low
    "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1": NormalDistribution(Attitude.NEUTRAL), #Medium
    "3fb4ae3d-c892-4025-815f-6b6074ac3d3c": NormalDistribution(Attitude.POSITIVE), #High

    # harvesting effort (8c7bd4d7-b91e-4518-99d4-7564df1d4207)
    "a755ba0d-fb8d-475a-a0f9-5ca267fd479f": NormalDistribution(Attitude.NEGATIVE), # Manual
    "653b4832-6647-426d-a18e-ee444ba67979": NormalDistribution(Attitude.NEUTRAL), # Harvester
    "dcb34d08-06f2-4426-a3a9-039cec1e6f6d": NormalDistribution(Attitude.NEUTRAL), # Self-driving Harvester

    # harvesting amount (c5b446ce-455a-44b5-b8be-178eef2848c2)
    "9e70ea9a-1311-48db-9238-cbc98da1ed2b": NormalDistribution(Attitude.NEGATIVE), #No harvest
    "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c": NormalDistribution(Attitude.NEGATIVE), #Low harvest
    "09594573-6fc5-4c62-9d5c-84b4ccf817a1": NormalDistribution(Attitude.POSITIVE), #High harvest

    # wood price (3a375746-288f-4147-8065-9f6966389772)
    "8d2f5efe-db35-4b4d-9591-cf797335e3ba": NormalDistribution(Attitude.POSITIVE), #Low
    "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93": NormalDistribution(Attitude.NEUTRAL), #Medium
    "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853": NormalDistribution(Attitude.NEGATIVE), #High   

    # public accessability (5d8ab41c-02bd-4478-9106-64e80bdb9728)
    "d59c52cf-0eb1-4ad9-9228-c5100c2b6237": NormalDistribution(Attitude.NEUTRAL), #Almost none
    "311389a2-c4b7-4a13-bf5a-04a1befad0e9": NormalDistribution(Attitude.NEUTRAL), #Low intensity
    "f08b7cd1-c470-4d6e-951d-a69a02b04849": NormalDistribution(Attitude.NEUTRAL), #High intensity
}