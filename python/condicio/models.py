from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Simple types
# ---------------------------------------------------------------------------

@dataclass
class Address:
    street: Optional[str] = None
    city: Optional[str] = None
    stateOrProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None


@dataclass
class ContactInfo:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None


# ---------------------------------------------------------------------------
# Document-level metadata
# ---------------------------------------------------------------------------

@dataclass
class ContractMetadata:
    title: str
    type: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = "en"
    jurisdiction: Optional[str] = None
    governingLaw: Optional[str] = None
    status: Optional[str] = None
    contractId: Optional[str] = None
    executionDate: Optional[str] = None
    effectiveDate: Optional[str] = None
    expiryDate: Optional[str] = None
    renewalTerms: Optional[str] = None
    amendmentSummary: Optional[str] = None


@dataclass
class Party:
    name: str
    role: str
    id: Optional[str] = None
    alias: Optional[str] = None
    type: Optional[str] = None
    jurisdiction: Optional[str] = None
    contact: Optional[ContactInfo] = None
    representative: Optional[ContactInfo] = None


@dataclass
class ContractDate:
    label: str
    date: str
    description: Optional[str] = None
    clauseRef: Optional[str] = None


@dataclass
class Clause:
    id: str
    text: str
    title: Optional[str] = None
    summary: Optional[str] = None
    type: Optional[str] = None
    scope: Optional[str] = None
    obligationRefs: Optional[list[str]] = None
    riskRefs: Optional[list[str]] = None
    confidence: Optional[float] = None


@dataclass
class Obligation:
    description: str
    obligor: str
    id: Optional[str] = None
    beneficiary: Optional[str] = None
    type: Optional[str] = None
    deadline: Optional[str] = None
    deadlineType: Optional[str] = None
    fixedDate: Optional[str] = None
    daysFromEvent: Optional[int] = None
    status: Optional[str] = None
    clauseRef: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class FinancialTerm:
    label: str
    amount: float
    currency: Optional[str] = None
    period: Optional[str] = None
    description: Optional[str] = None
    clauseRef: Optional[str] = None


@dataclass
class Payment:
    dueDate: str
    amount: float
    description: Optional[str] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    paidDate: Optional[str] = None


@dataclass
class Financials:
    currency: Optional[str] = None
    terms: Optional[list[FinancialTerm]] = None
    totalContractValue: Optional[float] = None
    paymentTerms: Optional[str] = None
    latePaymentPenalty: Optional[str] = None
    paymentSchedule: Optional[list[Payment]] = None


@dataclass
class Risk:
    description: str
    severity: str
    id: Optional[str] = None
    category: Optional[str] = None
    impact: Optional[str] = None
    mitigation: Optional[str] = None
    affectedParty: Optional[str] = None
    clauseRef: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class Definition:
    term: str
    definition: str
    clauseRef: Optional[str] = None


@dataclass
class SourceDocument:
    filename: Optional[str] = None
    mediaType: Optional[str] = None
    size: Optional[int] = None
    pages: Optional[int] = None
    hash: Optional[dict[str, str]] = None
    uri: Optional[str] = None


@dataclass
class ExtractionEngine:
    name: Optional[str] = None
    version: Optional[str] = None


@dataclass
class Metadata:
    extractedAt: Optional[str] = None
    extractedBy: Optional[str] = None
    extractionEngine: Optional[ExtractionEngine] = None
    confidence: Optional[float] = None
    sourceDocument: Optional[SourceDocument] = None
    tags: Optional[list[str]] = None
    custom: Optional[Any] = None


@dataclass
class CondicioDocument:
    condicio: str
    specVersion: str
    contract: ContractMetadata
    parties: list[Party]
    id: Optional[str] = None
    dates: Optional[list[ContractDate]] = None
    clauses: Optional[list[Clause]] = None
    obligations: Optional[list[Obligation]] = None
    financials: Optional[Financials] = None
    risks: Optional[list[Risk]] = None
    definitions: Optional[list[Definition]] = None
    metadata: Optional[Metadata] = None


# ---------------------------------------------------------------------------
# Deserialization helpers
# ---------------------------------------------------------------------------

def _optional(cls, data):
    if data is None:
        return None
    return cls(**data)


def _list_of(cls, data):
    if data is None:
        return None
    return [cls(**item) for item in data]


def document_from_dict(data: dict) -> CondicioDocument:
    return CondicioDocument(
        condicio=data.get("condicio", ""),
        specVersion=data.get("specVersion", ""),
        id=data.get("id"),
        contract=ContractMetadata(**data["contract"]),
        parties=_list_of(Party, data.get("parties", [])),
        dates=_list_of(ContractDate, data.get("dates")),
        clauses=_list_of(Clause, data.get("clauses")),
        obligations=_list_of(Obligation, data.get("obligations")),
        financials=_optional(Financials, data.get("financials")),
        risks=_list_of(Risk, data.get("risks")),
        definitions=_list_of(Definition, data.get("definitions")),
        metadata=_optional(Metadata, data.get("metadata")),
    )
