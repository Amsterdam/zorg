from datasets.general import documents as docs
import models


def buuv_to_activiteit(buuv: models.Buuv) -> docs.NormalizedActiviteit:
    doc = docs.NormalizedActiviteit(_id=buuv.id)
    doc.naam = buuv.naam
    doc.tags = buuv.type
    doc.beschrijving = buuv.omschrijving

    return doc
