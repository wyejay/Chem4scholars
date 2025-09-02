
import requests
BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def fetch_compound(name: str):
    if not name: return None
    try:
        r = requests.get(f"{BASE}/compound/name/{name}/cids/JSON", timeout=10)
        if r.status_code != 200: return None
        data = r.json()
        cids = data.get("IdentifierList", {}).get("CID", [])
        if not cids: return None
        cid = cids[0]
        props = requests.get(
            f"{BASE}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName,CanonicalSMILES/JSON",
            timeout=10
        )
        pjson = props.json()
        rec = pjson.get("PropertyTable", {}).get("Properties", [{}])[0]
        return {
            "cid": cid,
            "name": rec.get("IUPACName") or name,
            "formula": rec.get("MolecularFormula"),
            "molar_mass": rec.get("MolecularWeight"),
            "smiles": rec.get("CanonicalSMILES"),
            "source": "PubChem"
        }
    except Exception:
        return None
