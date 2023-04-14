# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.orm import Mapped, mapped_column

from power_systems_data_api_demonstrator.src.lib.db.base import Base


class GridNodeModel(Base):
    """Model of a grid node."""

    __tablename__ = "grid_node"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
