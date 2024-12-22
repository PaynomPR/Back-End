import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.taxes import FixedTaxes

from schemas.fixed_taxes import FixedTaxeIDShema, FixedTaxeShema
from passlib.context import CryptContext



taxes_router = APIRouter()



def create_fixed_taxe_controller(taxe_data):
    try:
        taxes_query = FixedTaxes(        
            name = taxe_data.name,
            amount = taxe_data.amount,
            limit = taxe_data.limit,
            is_deleted = False,  
            )     
        
        session.add(taxes_query)
        session.commit()
        session.refresh(taxes_query)   
        return {"ok": True, "msg": "Taxes was successfully created", "result": taxes_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def delete_taxe_controller(taxes_id):
    try:    
        taxe_query = session.query(FixedTaxes).filter(FixedTaxes.id == taxes_id).first()
        taxe_query.is_deleted = not taxe_query.is_deleted    
        taxe_query.deleted_at = datetime.utcnow()
        session.add(taxe_query)   
        session.commit()  
        session.refresh(taxe_query)   
        return {"ok": True, "msg": "user was successfully created", "result": taxe_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()

def get_fixed_taxes_controller():
    try:
        taxe_query = session.query(FixedTaxes).all()

        return {
            "ok": True,
            "msg": "Taxe were successfully retrieved",
            "result": taxe_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()



def get_fixed_taxes_by_id_controller(taxes_id):
    try:
        taxe_query = session.query(FixedTaxes).filter(FixedTaxes.id == taxes_id).first()

        return {
            "ok": True,
            "msg": "Taxe were successfully retrieved",
            "result": taxe_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()



def update_taxe_controller(taxe_id, taxe):
    try:
        taxes_query = session.query(FixedTaxes).filter(FixedTaxes.id==taxe_id).first()
            
        taxes_query.amount = taxe.amount,   
        taxes_query.limit = taxe.limit,  
        session.add(taxes_query)
        session.commit()
        session.refresh(taxes_query)

        return {"ok": True, "msg": "Taxe was successfully updated", "result": taxes_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()
        
        