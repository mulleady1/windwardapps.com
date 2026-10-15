const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  BorderStyle, ShadingType, AlignmentType, ImageRun, LevelFormat, VerticalAlign,
  Footer, ExternalHyperlink, TableLayoutType,
} = require('docx');

const NAVY = '172E53', OCEAN = '176FB3', PALM = '2E9E4B', INK = '15243D', TEXT = '2C3A50',
      MUTED = '5F6C80', LINE = 'E3E8EF', SAND = 'F7F5F0', PALMSOFT = 'E6F7DF';
const FONT = 'Arial';
const PAGE_W = 12240, MARGIN = 1008; // 0.7in
const CONTENT_W = PAGE_W - 2 * MARGIN; // 10224
const MAIN_W = 6624, SIDE_W = CONTENT_W - MAIN_W; // 3600
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
const cellNone = { top: none, bottom: none, left: none, right: none };

const t = (text, o = {}) => new TextRun({ text, font: FONT, size: 18, color: TEXT, ...o });
const ph = (text) => new TextRun({ text, font: FONT, size: 18, color: '7A5A00', shading: { type: ShadingType.CLEAR, fill: 'FFF3B0', color: 'auto' } });
const p = (children, o = {}) => new Paragraph({ spacing: { after: 80, line: 264 }, ...o, children: Array.isArray(children) ? children : [children] });

const h2 = (text) => new Paragraph({
  spacing: { before: 160, after: 80 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: OCEAN, space: 2 } },
  children: [new TextRun({ text: text.toUpperCase(), font: FONT, size: 18, bold: true, color: NAVY, characterSpacing: 20 })],
});
const sideH = (text) => new Paragraph({
  spacing: { before: 180, after: 60 },
  children: [new TextRun({ text: text.toUpperCase(), font: FONT, size: 15, bold: true, color: OCEAN, characterSpacing: 20 })],
});
const bullet = (lead, rest) => new Paragraph({
  numbering: { reference: 'bullets', level: 0 },
  spacing: { after: 40, line: 240 },
  children: [
    ...(lead ? [new TextRun({ text: lead + ' ', font: FONT, size: 18, bold: true, color: INK })] : []),
    ...(Array.isArray(rest) ? rest : [t(rest)]),
  ],
});
const kv = (k, v) => new Paragraph({
  spacing: { after: 40, line: 252 },
  children: [
    new TextRun({ text: k, font: FONT, size: 16, color: MUTED }),
    new TextRun({ text: '  ', font: FONT, size: 16 }),
    ...(Array.isArray(v) ? v : [new TextRun({ text: v, font: FONT, size: 17, bold: true, color: INK })]),
  ],
});
const small = (text, o = {}) => new Paragraph({ spacing: { after: 30, line: 252 }, children: [new TextRun({ text, font: FONT, size: 16, color: TEXT, ...o })] });

// ----- Header block: logo + title -----
const logo = fs.readFileSync('logo.png');
const headerTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [MAIN_W, SIDE_W], borders: noBorders, layout: TableLayoutType.FIXED,
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: MAIN_W, type: WidthType.DXA }, borders: cellNone, verticalAlign: VerticalAlign.CENTER, margins: { left: 0 }, children: [
      new Paragraph({ spacing: { after: 0 }, children: [new ImageRun({ type: 'png', data: logo, transformation: { width: 232, height: 50 } })] }),
    ] }),
    new TableCell({ width: { size: SIDE_W, type: WidthType.DXA }, borders: cellNone, verticalAlign: VerticalAlign.CENTER, margins: { right: 0 }, children: [
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 20 }, children: [new TextRun({ text: 'CAPABILITY STATEMENT', font: FONT, size: 22, bold: true, color: NAVY, characterSpacing: 30 })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [new TextRun({ text: 'SDVOSB  ·  SBA VetCert certified', font: FONT, size: 16, color: PALM, bold: true })] }),
    ] }),
  ] })],
});

const tagline = new Paragraph({
  spacing: { before: 200, after: 60 },
  children: [new TextRun({ text: 'Enterprise-scale systems for government, in months, not years.', font: FONT, size: 28, bold: true, color: NAVY })],
});
const overview = p([
  t('Windward Apps is a service-disabled veteran-owned software consultancy in Kailua, Hawaiʻi. We build and modernize the systems agencies actually run on: custom applications, public portals, data pipelines, automation, and AI integration. Our engineers direct AI agents that write, test and refactor code, and a senior engineer reviews every line before it ships. That is how a small team delivers enterprise-scale work in months instead of years, at a fraction of the traditional cost.'),
], { spacing: { after: 100, line: 252 } });

// ----- Main column -----
const main = [
  h2('Core competencies'),
  bullet('Custom applications.', 'Public portals, case and workflow management, field data collection, internal tools, and the integrations between them. Web first; native iOS and Android when needed.'),
  bullet('Modernization and automation.', 'Incremental replacement of paper, fax, spreadsheet and legacy processes, with data kept intact and hand-offs automated.'),
  bullet('Data and reporting.', 'Pipelines that pull from existing systems into one source of truth, feeding dashboards and required reporting automatically.'),
  bullet('AI integration.', 'Document intake, summarization and search across agency records; MCP servers that let an assistant act on existing tools. Access controls and audit trails included.'),
  bullet('Cloud and operations.', 'Deployment, infrastructure automation, and ongoing operations, with the agency owning every account.'),
  bullet('GIS, desktop and hardware.', 'Geographic information systems, desktop software, embedded devices.'),

  h2('Differentiators'),
  bullet('Agent-driven development.', 'AI agents do the hours behind every feature. Budgets that used to buy a requirements study now buy a finished system.'),
  bullet('Senior accountability.', 'A senior engineer directs the work and reviews every line of code. No junior bench, no hand-offs.'),
  bullet('Working software early.', 'Something to review within the first sprint, then short iterations until delivery.'),
  bullet('Scope you can trust.', 'A short discovery phase first, then firm-fixed-price for defined scope. Time-and-materials for support and evolving work.'),
  bullet('You own everything.', 'Code, data and infrastructure accounts belong to the agency from day one.'),
  bullet('SDVOSB.', 'Eligible for set-aside and sole-source awards. Prime or subcontractor.'),

  h2('Past performance'),
  pp('Hawaiʻi Department of Health', 'COVID-19 vaccine reporting pipeline', [
    t('With the first vaccine shipments en route in late 2020 and the state immunization registry offline, the CDC required every vaccination event reported before approving further shipments. Working with DOH, the State Epidemiologist and the CDC, designed and built the ETL tool that pulled records from CDC\u2019s VAMS and produced the daily datasets CDC required. Six months through handoff, as subcontractor to Hawaiʻi Data Collaborative.'),
  ], 'Hawaiʻi Data Collaborative; contact details on request'),
  pp('Hawaiʻi Commission on Water Resource Management', 'GIS software', [
    t('Custom geographic information system software for the State of Hawaiʻi agency, under the Department of Land and Natural Resources, that regulates the state\u2019s water resources.'),
  ], 'Roy Hardy, roy.hardy@hawaii.gov'),
  pp('Shine Rite', 'On-demand mobile car-wash marketplace', [
    t('Customer and provider mobile apps with scheduling, dispatch and payments. Launched and ran in production in Texas for several years.'),
  ], 'Trevor Williams, trevorwilliamsatx@gmail.com'),
];
function pp(org, project, scope, poc) {
  return [
    new Paragraph({ spacing: { before: 60, after: 20 }, children: [
      new TextRun({ text: org, font: FONT, size: 18, bold: true, color: INK }),
      new TextRun({ text: '  ·  ' + project, font: FONT, size: 18, color: MUTED }),
    ] }),
    new Paragraph({ spacing: { after: 20, line: 240 }, children: scope }),
    new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: 'Reference: ' + poc, font: FONT, size: 15, color: MUTED })] }),
  ];
}

// ----- Sidebar -----
const side = [
  sideH('Company data'),
  kv('UEI', 'LVJ7FKGSFLF4'),
  kv('CAGE', '84XP7'),
  kv('SAM.gov', 'Active'),
  kv('Status', 'SDVOSB, SBA VetCert certified'),
  kv('Size', 'Small business, all listed NAICS'),
  kv('Role', 'Prime and subcontractor'),
  kv('Contracts', 'Firm-fixed-price, T&M'),
  kv('Founded', '2018'),

  sideH('NAICS codes'),
  kv('541511', [new TextRun({ text: 'Custom programming  ', font: FONT, size: 16, color: INK }), new TextRun({ text: 'PRIMARY', font: FONT, size: 12, bold: true, color: PALM })]),
  kv('541512', [new TextRun({ text: 'Computer systems design', font: FONT, size: 16, color: INK })]),
  kv('541519', [new TextRun({ text: 'Other computer related services', font: FONT, size: 16, color: INK })]),
  kv('518210', [new TextRun({ text: 'Computing infrastructure, hosting', font: FONT, size: 16, color: INK })]),
  kv('541611', [new TextRun({ text: 'Management consulting', font: FONT, size: 16, color: INK })]),
  kv('541690', [new TextRun({ text: 'Technical consulting', font: FONT, size: 16, color: INK })]),

  sideH('Product and service codes'),
  small('DA01  Application development support'),
  small('DF01  IT management support'),
  small('DH01  Platform support'),
  small('DE02  Mobile device support'),
  small('B506  Studies and analysis: data'),
  small('B544  Studies and analysis: technology'),

  sideH('Contact'),
  new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: 'Kyle Mulleady, Founder', font: FONT, size: 17, bold: true, color: INK })] }),
  small('(808) 298-8419'),
  small('kyle@windwardapps.com'),
  small('windwardapps.com'),
  new Paragraph({ spacing: { before: 60, after: 0 }, children: [new TextRun({ text: 'Windward Apps', font: FONT, size: 16, color: TEXT })] }),
  small('74 Kihapai St'),
  small('Kailua, HI 96734'),
];

const body = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [MAIN_W, SIDE_W], borders: noBorders, layout: TableLayoutType.FIXED,
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: MAIN_W, type: WidthType.DXA }, borders: cellNone, margins: { left: 0, right: 360, top: 0, bottom: 0 }, children: main.flat() }),
    new TableCell({ width: { size: SIDE_W, type: WidthType.DXA }, borders: cellNone, shading: { type: ShadingType.CLEAR, fill: SAND, color: 'auto' }, margins: { left: 260, right: 260, top: 80, bottom: 200 }, children: side }),
  ] })],
});

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 18, color: TEXT } } } },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 240, hanging: 240 } }, run: { color: OCEAN } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 15840 }, margin: { top: 720, bottom: 620, left: MARGIN, right: MARGIN, footer: 400 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
      children: [new TextRun({ text: 'Windward Apps  ·  Service-disabled veteran-owned small business  ·  UEI LVJ7FKGSFLF4  ·  CAGE 84XP7  ·  windwardapps.com', font: FONT, size: 14, color: MUTED })] })] }) },
    children: [headerTable, tagline, overview, body],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync('Windward Apps Capability Statement.docx', b); console.log('wrote', b.length, 'bytes'); });
