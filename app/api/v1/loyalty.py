from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ...models import get_db
from ...schemas.loyalty import LoyaltyConfig, LoyaltyConfigUpdate, LoyaltyTransaction, LoyaltyTransactionCreate
from ...repositories.loyalty_repo import LoyaltyRepository
from ...dependencies import get_current_tenant

router = APIRouter()

@router.get("/config", response_model=LoyaltyConfig)
async def get_loyalty_config(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant)
):
    repo = LoyaltyRepository(db)
    return await repo.get_config(tenant_id)

@router.put("/config", response_model=LoyaltyConfig)
async def update_loyalty_config(
    update_data: LoyaltyConfigUpdate,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant)
):
    repo = LoyaltyRepository(db)
    return await repo.update_config(tenant_id, update_data)

@router.get("/transactions/{customer_id}", response_model=List[LoyaltyTransaction])
async def get_customer_loyalty_transactions(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant)
):
    repo = LoyaltyRepository(db)
    return await repo.get_customer_transactions(tenant_id, customer_id)

@router.post("/transactions", response_model=LoyaltyTransaction)
async def add_loyalty_transaction(
    trans_data: LoyaltyTransactionCreate,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_current_tenant)
):
    repo = LoyaltyRepository(db)
    return await repo.add_transaction(tenant_id, trans_data)
