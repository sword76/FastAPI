from typing import Any
from pydantic import BaseModel
from sqlalchemy import select, exists, inspect, update, func
from sqlalchemy.ext.asyncio import AsyncSession

class Repository:
    def init(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def editone(self, data: BaseModel, filterby) -> None:
        # 1) Определяем PK колонки у модели
        mapper = inspect(self.model)
        pkcols = mapper.primarykey
        print("DEBUG: mapper.primarykey:", pkcols)
        if len(pkcols) != 1:
            raise NotImplementedError("Метод поддерживает только одну колонку PK")
        pkcol = pkcols0
        pkname = pkcol.key
        print("DEBUG: pkname:", pkname)

        # 2) Извлекаем значение id: в приоритете filterby, затем поле в data
        idval = None
        if pkname in filterby:
            idval = filterby
            print(f"DEBUG: id found in filterby[{pkname}]:", idval)
        elif 'id' in filterby:
            idval = filterby'id'
            print("DEBUG: id found in filterby['id']:", idval)
        else:
            idval = getattr(data, pkname, None)
            print(f"DEBUG: id from getattr(data, '{pkname}'):", idval)
            if idval is None and hasattr(data, "dict"):
                dd = data.dict(excludeunset=True)
                print("DEBUG: data.dict(excludeunset=True):", dd)
                idval = dd.get(pkname) or dd.get("id")
                print("DEBUG: id from data.dict():", idval)

        if idval is None:
            raise ValueError("Не удалось определить идентификатор. Передайте id в filterby или в data.")

        # 3) Проверка на дубликаты значений PK (неожиданная ситуация)
        #    Выполняем эффективный запрос: найти любое значение PK, которое встречается >1 раза.
        dupstmt = (
            select(pkcol)
            .groupby(pkcol)
            .having(func.count() > 1)
            .limit(1)
        )
        print("DEBUG: duplicate-check statement:", dupstmt)
        dupres = await self.session.execute(dupstmt)
        dupval = dupres.scalar()  # вернёт значение PK при наличии дубликата или None
        print("DEBUG: duplicate value found (if any):", dupval)
        if dupval is not None:
            # Дубликаты PK — серьёзная проблема целостности данных
            raise RuntimeError(
                f"Data integrity error: duplicate values found for primary key column '{pkname}'. "
                f"Example duplicate value: {dupval}"
            )

        # 4) Проверяем существование записи (exists)
        existsstmt = select(exists().where(pkcol == idval))
        print("DEBUG: existsstmt:", existsstmt)
        existsbool = await self.session.scalar(existsstmt)
        print("DEBUG: existsbool:", existsbool)

        if not existsbool:
            raise LookupError(f"{self.model.name} with {pkname}={idval} not found")

        # 5) Формируем словарь обновляемых значений из Pydantic модели
        updatevalues = data.dict(excludeunset=True)
        print("DEBUG: raw updatevalues from data:", updatevalues)
        updatevalues.pop(pkname, None)
        updatevalues.pop("id", None)
        print("DEBUG: updatevalues after popping PK:", updatevalues)

        if not updatevalues:
            print("DEBUG: Nothing to update (no fields set). Exiting.")
            return

        # 6) Выполняем UPDATE
        stmt = update(self.model).where(pkcol == idval).values(**updatevalues)
        print("DEBUG: UPDATE statement (SQLAlchemy):", stmt)
        result = awa