#!/usr/bin/env node
// Gera um mapa SVG estático (paths prontos para animar com GSAP) a partir de dados abertos.
//
// Uso:
//   node ferramentas/mapa.mjs --bbox -75,-20,-56,-2 --largura 960 --altura 860 \
//        --paises Brazil,Bolivia,Peru --estados Acre,Amazonas,Rondônia --rios Purus,Juruá,Madeira \
//        --pontos "Xapuri:-68.50,-10.65;Rio Branco:-67.81,-9.97" --saida mapa.svg
//
// Países: Natural Earth via npm `world-atlas` (domínio público). Estados do Brasil:
// ferramentas/dados/brasil-estados.geojson (IBGE, via click_that_hood). Rios: Natural Earth 10m.
// Subdivisões fora do Brasil (--regioes "Massachusetts,Scotland"): ferramentas/dados/subdivisoes-ne10m.geojson,
// recorte de Natural Earth 10m (admin-1 e map units; hoje Nova Inglaterra + NY e as 4 nações do Reino Unido).
// Cada forma sai com id estável: pais-bolivia, uf-acre, rio-madeira, ponto-xapuri.
// O JSON ao lado (mesmo nome .json) traz centroides e pontos projetados para posicionar rótulos.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { geoMercator, geoPath, geoCentroid, geoArea } from "d3-geo";
import { feature } from "topojson-client";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => (a.startsWith("--") ? [...acc, [a.slice(2), arr[i + 1]?.startsWith("--") || arr[i + 1] === undefined ? true : arr[i + 1]]] : acc), []),
);
const slug = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-");
const [x0, y0, x1, y1] = String(args.bbox || "-75,-20,-56,-2").split(",").map(Number);
const W = Number(args.largura || 960), H = Number(args.altura || 860);
const caixa = { type: "Feature", geometry: { type: "Polygon", coordinates: [[[x0, y0], [x0, y1], [x1, y1], [x1, y0], [x0, y0]]] } };
const proj = geoMercator().fitExtent([[0, 0], [W, H]], caixa);
const gp = geoPath(proj).digits(1);

const topo = JSON.parse(fs.readFileSync(path.join(aqui, "node_modules/world-atlas/countries-50m.json"), "utf8"));
const paises = feature(topo, topo.objects.countries).features;
const ufs = JSON.parse(fs.readFileSync(path.join(aqui, "dados/brasil-estados.geojson"), "utf8")).features;

const partes = [], meta = { largura: W, altura: H, bbox: [x0, y0, x1, y1], centroides: {}, pontos: {} };
// d3 espera anéis no sentido horário; GeoJSON comum vem no anti-horário (vira "o mundo menos a forma").
const rewind = (f) => {
  if (geoArea(f) <= 2 * Math.PI) return f;
  const g = f.geometry, rev = (polys) => polys.map((rings) => rings.map((r) => [...r].reverse()));
  const coords = g.type === "Polygon" ? rev([g.coordinates])[0] : rev(g.coordinates);
  return { ...f, geometry: { ...g, coordinates: coords } };
};
const add = (cls, id, f) => {
  f = rewind(f);
  const d = gp(f);
  if (!d) return;
  partes.push(`<path id="${id}" class="${cls}" d="${d}"/>`);
  meta.centroides[id] = proj(geoCentroid(f)).map((v) => Math.round(v));
};

for (const nome of String(args.paises || "").split(",").filter(Boolean)) {
  const f = paises.find((p) => p.properties.name.toLowerCase() === nome.toLowerCase());
  if (!f) { console.error(`✗ país não encontrado: ${nome}`); process.exit(1); }
  add("pais", `pais-${slug(nome)}`, f);
}
for (const nome of String(args.estados || "").split(",").filter(Boolean)) {
  const f = ufs.find((p) => slug(p.properties.name) === slug(nome));
  if (!f) { console.error(`✗ estado não encontrado: ${nome}`); process.exit(1); }
  add("uf", `uf-${slug(nome)}`, f);
}
for (const nome of String(args.regioes || "").split(",").filter(Boolean)) {
  const regs = JSON.parse(fs.readFileSync(path.join(aqui, "dados/subdivisoes-ne10m.geojson"), "utf8")).features;
  const f = regs.find((p) => slug(p.properties.name) === slug(nome));
  if (!f) { console.error(`✗ região não encontrada: ${nome}`); process.exit(1); }
  add("pais", `reg-${slug(nome)}`, f);
}
if (args.rios) {
  const rios = JSON.parse(fs.readFileSync(path.join(aqui, "dados/rios.geojson"), "utf8")).features;
  const dentro = ([lon, lat]) => lon >= x0 && lon <= x1 && lat >= y0 && lat <= y1;
  for (const r of rios) {
    const g = r.geometry, linhas = g.type === "LineString" ? [g.coordinates] : g.type === "MultiLineString" ? g.coordinates : [];
    if (!linhas.some((l) => l.some(dentro)) || r.properties.featurecla !== "River") continue;
    const nome = r.properties.name || "rio";
    if (args.rios !== true && !String(args.rios).split(",").some((n) => slug(n) === slug(nome))) continue;
    const d = gp(r);
    if (d) partes.push(`<path id="rio-${slug(nome)}" class="rio" d="${d}"/>`);
  }
}
for (const par of String(args.pontos || "").split(";").filter(Boolean)) {
  const [nome, coord] = par.split(":");
  const [lon, lat] = coord.split(",").map(Number);
  const [px, py] = proj([lon, lat]).map((v) => Math.round(v));
  meta.pontos[`ponto-${slug(nome)}`] = { nome, x: px, y: py };
}

// --pontos-em uf-acre:240  → pontos pseudoaleatórios (semente fixa) dentro de uma forma, já projetados
if (args["pontos-em"]) {
  const [alvo, qtd] = String(args["pontos-em"]).split(":");
  const nomeAlvo = alvo.replace(/^(uf|pais)-/, "");
  const f = rewind(alvo.startsWith("uf-") ? ufs.find((p) => slug(p.properties.name) === nomeAlvo) : paises.find((p) => slug(p.properties.name) === nomeAlvo));
  let s = 42; const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  const { geoContains, geoBounds } = await import("d3-geo");
  const [[lo0, la0], [lo1, la1]] = geoBounds(f);
  meta.pontosEm = [];
  for (let i = 0; meta.pontosEm.length < Number(qtd) && i < 200000; i++) {
    const p = [lo0 + rnd() * (lo1 - lo0), la0 + rnd() * (la1 - la0)];
    if (geoContains(f, p)) meta.pontosEm.push(proj(p).map((v) => Math.round(v)));
  }
}
const svg = `<svg class="mapa" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">\n${partes.join("\n")}\n</svg>\n`;
const saida = args.saida || "mapa.svg";
fs.writeFileSync(saida, svg);
fs.writeFileSync(saida.replace(/\.svg$/, ".json"), JSON.stringify(meta, null, 1));
console.log(`✓ ${saida}: ${partes.length} formas · ${(svg.length / 1024).toFixed(0)} KB`);
