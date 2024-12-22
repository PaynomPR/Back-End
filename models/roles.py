# from typing import List
# from sqlalchemy import TIMESTAMP, Integer, String, Boolean, func
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import relationship
#
# from database.config import Base
# from models.users import User
#
#
# class Role(Base):
#     __tablename__ = "roles"
#
#     id: Mapped[int] = mapped_column(
#         Integer, primary_key=True, autoincrement=True, index=True
#     )
#     role: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
#     is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
#     deleted_at: Mapped[TIMESTAMP] = mapped_column(
#         TIMESTAMP(timezone=False), nullable=True
#     )
#     created_at: Mapped[TIMESTAMP] = mapped_column(
#         TIMESTAMP(timezone=False), server_default=func.now(), nullable=False
#     )
#     update_at: Mapped[TIMESTAMP] = mapped_column(
#         TIMESTAMP(timezone=False),
#         nullable=True,
#         onupdate=func.now(),
#     )
#
#     user: Mapped["User"] = relationship(back_populates="roles")

# User = relationship("User", back_populates="users")
