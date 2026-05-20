import asyncio
from playwright.async_api import async_playwright
import yaml

async def extreure_resultats():
    url = "https://www.laliga.com/es-GB/laliga-easports/resultados"
    
    async with async_playwright() as p:
        # Obrim el navegador en mode 'headless' (sense interfície gràfica)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"S'està connectant a: {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # Opcional: Acceptar galetes si apareix el contingut molest
        try:
            await page.click("#onetrust-accept-btn-handler", timeout=3000)
        except:
            pass # Si no apareix o ja s'ha tancat, continuem

        # Esperem que els blocs de partits es renderitzin a la pantalla
        # Nota: Els selectors CSS de LaLiga poden variar, utilitzem l'estructura de contenidors de partits comuns.
        await page.wait_for_selector("div.styled__MatchContainer-sc-", timeout=10000)
        
        # Busquem tots els contenidors de partits de la jornada actual
        partits_elements = await page.query_selector_all("div.styled__MatchContainer-sc-")
        
        llista_partits = []
        
        for idx, partit in enumerate(partits_elements, start=1):
            try:
                # Extreure els noms dels equips (local i visitant)
                # Busquem etiquetes que continguin el nom o escuts (es pot ajustar el selector segons l'estructura exacta)
                equips = await partit.query_selector_all("p.styled__TextRegular-sc-") 
                # Solen haver-hi paràgrafs per l'estat, equip 1, equip 2, etc.
                
                # Exemple de lògica adaptada a l'estructura dinàmica:
                nom_local = await equips[0].inner_text() if len(equips) > 0 else "Desconegut"
                nom_visitant = await equips[1].inner_text() if len(equips) > 1 else "Desconegut"
                
                # Extreure els marcadors/gols
                gols_elements = await partit.query_selector_all("p.styled__Score-sc-") # Selector del marcador
                if len(gols_elements) >= 2:
                    gols_local = int(await gols_elements[0].inner_text())
                    gols_visitant = int(await gols_elements[1].inner_text())
                    estat = "Finalitzat"
                else:
                    gols_local = None
                    gols_visitant = None
                    estat = "Planificat"
                
                # Afegir a la llista estructurada
                llista_partits.append({
                    "id": idx,
                    "estat": estat,
                    "equip_local": {
                        "nom": nom_local.strip(),
                        "gols": gols_local
                    },
                    "equip_visitant": {
                        "nom": nom_visitant.strip(),
                        "gols": gols_visitant
                    }
                })
            except Exception as e:
                # Si un partit en concret falla pel selector, continuem amb els altres
                print(f"Error processant el partit {idx}: {e}")
                continue
                
        # Estructura final en format diccionari
        dades_laliga = {
            "competicio": "LaLiga EA Sports",
            "temporada": "2025-2026",
            "partits": llista_partits
        }
        
        # Tanquem el navegador
        await browser.close()
        
        # Desem el resultat en un fitxer YAML de sortida
        with open("resultats_extrets.yaml", "w", encoding="utf-8") as f:
            yaml.dump(dades_laliga, f, allow_unicode=True, default_flow_style=False)
            
        print("S'ha completat l'extracció! Dades desades a 'resultats_extrets.yaml'")

# Executar la funció asíncrona
asyncio.run(extreure_resultats())
