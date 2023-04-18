# SPDX-License-Identifier: Apache-2.0

from typing import List, cast

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from power_systems_data_api_demonstrator.src.api.grid_node.schema import (
    CapacityDTO,
    DayAheadPriceDTO,
    DemandDTO,
    ExchangeDTO,
    FuelTypes,
    GridNodeModelDTO,
)
from power_systems_data_api_demonstrator.src.lib.db.dao.grid_node_dao import (
    GenerationDTO,
    GridNodeDAO,
    GridNodeNotFoundError,
)
from power_systems_data_api_demonstrator.src.lib.db.models.demand import DemandModel
from power_systems_data_api_demonstrator.src.lib.db.models.exchanges import (
    ExchangeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.grid_node_model import (
    GridNodeModel,
)
from power_systems_data_api_demonstrator.src.lib.db.models.prices import (
    DayAheadPriceModel,
)

router = APIRouter()


@router.get("/list", response_model=List[GridNodeModelDTO])
async def list_grid_nodes(
    limit: int = 10,
    grid_node_dao: GridNodeDAO = Depends(),
) -> List[GridNodeModel]:
    """
    Retrieve all grid nodes from the database.

    :param limit: limit of grid nodes, defaults to 10.
    :param grid_node_dao: DAO for grid nodes.
    :return: list of grid nodes from database.
    """
    return await grid_node_dao.get_all_grid_nodes(limit=limit)


@router.get("/describe/{id}", response_model=GridNodeModelDTO)
async def describe_grid_nodes(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> GridNodeModel:
    """
    Retrieve a description of a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_by_id(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get("/capacity/{id}", response_model=list[CapacityDTO])
async def get_capacity_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> list[CapacityDTO]:
    """
    Retrieve generation data for a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        raw_capacities = await grid_node_dao.get_capacity(id)
        capacity = []
        # Filter by datetime
        dts = set([cap.datetime for cap in raw_capacities])
        # This is error prone if we don't have all fuel types for all datetimes
        # Or with different units
        for dt in dts:
            capacities = [cap for cap in raw_capacities if cap.datetime == dt]
            capacity.append(
                CapacityDTO(
                    grid_node_id=id,
                    datetime=dt,
                    generation_capacity={
                        cast(FuelTypes, cap.fuel_type): cap.value for cap in capacities
                    },
                    unit=capacities[0].unit,
                )
            )
        return capacity
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


# TODO define generation model and return
@router.get("/generation/{id}", response_model=list[GenerationDTO])
async def get_generation_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> list[GenerationDTO]:
    """
    Retrieve generation data for a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_generation(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


# TODO define demand model and return
@router.get("/demand/{id}", response_model=list[DemandDTO])
async def get_demand_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> list[DemandModel]:
    """
    Retrieve demand data for a single grid node.

    :param id: id of a specific grid node.
    :param grid_node_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_demand(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get("/dayAheadPrice/{id}", response_model=List[DayAheadPriceDTO])
async def get_day_ahead_price_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> List[DayAheadPriceModel]:
    """
    Retrieve demand data for a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_day_ahead_price(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get("/imports/{id}", response_model=list[ExchangeDTO])
async def get_imports_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> list[ExchangeModel]:
    """
    Retrieve generation data for a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_imports(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None


@router.get("/exports/{id}", response_model=list[ExchangeDTO])
async def get_exports_grid_node(
    id: str,
    grid_node_dao: GridNodeDAO = Depends(),
) -> list[ExchangeModel]:
    """
    Retrieve generation data for a single grid node.

    :param id: id of a specific grid node.
    :param dummy_dao: DAO for grid nodes.
    :return: a single grid node with the given id.
    """
    try:
        return await grid_node_dao.get_exports(id)
    except GridNodeNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from None
