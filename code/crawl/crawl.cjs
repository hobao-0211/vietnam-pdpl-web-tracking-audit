// K7 crawler (G5). Chạy trên HOST (flatpak-spawn --host), điểm đo = IP Việt Nam của máy tác giả.
// node crawl.cjs <sites.tsv> <out_dir> [--par 4] [--wait 15] [--limit N]
//   sites.tsv: domain \t origin \t stratum   (có header)
// Mỗi site:
//   A, B: 2 context sạch, nạp origin, KHÔNG tương tác, chờ WAIT giây  -> request/cookie/storage
//   A còn: ảnh chụp, DOM text, dò banner/nút từ chối/link chính sách, tải văn bản chính sách (render)
//   C: chỉ khi thấy nút "từ chối": nạp, bấm từ chối, chờ WAIT giây, ghi request SAU khi bấm
// Ghi: out/sites.jsonl (1 dòng/site/profile), out/policy/<domain>.txt (chỉ dùng nội bộ), out/shots/<domain>.jpg
// Checkpoint: bỏ qua domain đã có dòng "done" trong out/done.txt. Heartbeat mỗi HB_EVERY giây (mặc định 60).
const fs = require('fs'), path = require('path');
const { chromium } = require(process.env.PW_DIR + '/node_modules/playwright');
process.on('unhandledRejection', e => console.log(new Date().toISOString().slice(11, 19), '[unhandled]', String(e).slice(0, 120)));
const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const [SITES, OUT] = argv;
const PAR = +opt('par', 4), WAIT = +opt('wait', 15) * 1000, LIMIT = +opt('limit', 1e9);
const NO_BLOCK_MEDIA = argv.includes('--no-block-media');  // phân tích độ nhạy (protocol §5): không chặn media
const PREPASS = argv.includes('--prepass');  // chỉ profile A, chờ WAIT, ghi tín hiệu site VN; không B/C/chính sách/ảnh
const HB = +(process.env.HB_EVERY || 60) * 1000;
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36';
for (const d of ['policy', 'shots']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
const doneF = path.join(OUT, 'done.txt');
const done = new Set(fs.existsSync(doneF) ? fs.readFileSync(doneF, 'utf8').split('\n').filter(Boolean) : []);
const sites = fs.readFileSync(SITES, 'utf8').split('\n').slice(1).filter(Boolean).map(l => { const [domain, origin, stratum] = l.split('\t'); return { domain, origin, stratum }; })
  .filter(s => !done.has(s.domain)).slice(0, LIMIT);
const out = fs.createWriteStream(path.join(OUT, 'sites.jsonl'), { flags: 'a' });
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);

const RE_BANNER = /cookie|quyền riêng tư|bảo mật dữ liệu|dữ liệu cá nhân|privacy/i;
const RE_CONSENTWORD = /(đồng ý|chấp nhận|accept|agree|cho phép|tiếp tục)/i;
const RE_REJECT = /^(từ chối( tất cả| hết)?|không đồng ý|không chấp nhận|không cho phép|tôi không đồng ý|chỉ (chấp nhận |dùng |sử dụng |cho phép )?(các )?cookie (cần thiết|bắt buộc)|chỉ (chấp nhận )?(cần thiết|bắt buộc)|reject( all)?|decline( all)?|refuse|deny|i disagree|disagree|necessary only|only necessary|accept only necessary( cookies)?|use necessary cookies only|continue without accepting)$/i;
const RE_POL_TXT = /chính sách (bảo mật|quyền riêng tư|riêng tư|bảo vệ dữ liệu|cookie|xử lý dữ liệu)|quyền riêng tư|bảo vệ dữ liệu cá nhân|privacy|cookie policy|điều khoản bảo mật/i;
const RE_POL_HREF = /privacy|chinh-sach-bao-mat|bao-mat-thong-tin|quyen-rieng-tu|bao-ve-du-lieu|chinh-sach-rieng-tu|du-lieu-ca-nhan|cookie/i;
const RE_CMP = /onetrust|cookielaw\.org|cookiebot|didomi|quantcast|cookieyes|osano|iubenda|trustarc|usercentrics|termly|consentmanager|cookie-?script|complianz|klaro|cookiehub/i;

let stat = { done: 0, ok: 0, fail: 0, active: {}, t0: Date.now(), total: sites.length };
setInterval(() => {
  const el = (Date.now() - stat.t0) / 1000, rate = stat.done / Math.max(el, 1);
  const eta = rate > 0 ? Math.round((stat.total - stat.done) / rate / 60) : -1;
  const mem = process.memoryUsage().rss / 1e6, free = memAvail() / 1e6;
  log(`[HB] ${Math.round(el / 60)}m | ${stat.done}/${stat.total} ok=${stat.ok} fail=${stat.fail} | ${(rate * 60).toFixed(1)} site/phút | ETA ${eta}m | node RSS ${mem.toFixed(0)}MB, RAM khả dụng ${free.toFixed(0)}MB | đang: ${Object.keys(stat.active).join(' ')}`);
}, HB).unref();

async function visit(browser, s, profile, { reject = false, detect = false, shot = true } = {}) {
  const ctx = await browser.newContext({ locale: 'vi-VN', timezoneId: 'Asia/Ho_Chi_Minh', userAgent: UA, viewport: { width: 1366, height: 768 }, ignoreHTTPSErrors: true });
  const page = await ctx.newPage();
  // Chặn tải luồng media (video/audio) để tiết kiệm RAM; request media VẪN được ghi (sự kiện 'request' xảy ra trước route)
  if (!NO_BLOCK_MEDIA) await page.route('**/*', r => r.request().resourceType() === 'media' ? r.abort() : r.continue()).catch(() => { });
  const reqs = []; const byReq = new WeakMap(); let clickedAt = null; const t0 = Date.now();
  page.on('request', r => { const e = { t: Date.now() - t0, url: r.url().slice(0, 2000), type: r.resourceType(), method: r.method(), frame: (() => { try { return r.frame().url().slice(0, 300); } catch { return ''; } })(), after_click: clickedAt !== null }; reqs.push(e); byReq.set(r, e); });
  page.on('response', async resp => {
    try {
      const e = byReq.get(resp.request()); if (!e) return;
      e.status = resp.status(); const sa = await resp.serverAddr(); e.ip = sa ? sa.ipAddress : null;
      const sc = (await resp.headersArray()).filter(h => h.name.toLowerCase() === 'set-cookie').map(h => h.value.slice(0, 400)); if (sc.length) e.set_cookie = sc;
    } catch { }
  });
  const rec = { domain: s.domain, origin: s.origin, stratum: s.stratum, profile, ts: new Date().toISOString(), ok: true };
  try {
    const resp = await page.goto(s.origin, { waitUntil: 'domcontentloaded', timeout: 45000 });
    rec.status = resp ? resp.status() : null;
    await page.waitForTimeout(reject ? 4000 : WAIT);
    rec.final_url = page.url();
    if (detect || reject) {
      const info = await page.evaluate(([rb, rc, rr, rpt, rph]) => {
        const RB = new RegExp(rb, 'i'), RC = new RegExp(rc, 'i'), RR = new RegExp(rr, 'i'), RPT = new RegExp(rpt, 'i'), RPH = new RegExp(rph, 'i');
        const vis = el => { const r = el.getBoundingClientRect(), st = getComputedStyle(el); return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none'; };
        const btns = [...document.querySelectorAll('button,a,[role=button],input[type=button],input[type=submit],div[onclick],span[onclick]')].filter(vis);
        const bt = btns.map(b => (b.innerText || b.value || '').trim().replace(/\s+/g, ' ')).filter(t => t && t.length < 60);
        // khối nổi (fixed/sticky) có chữ cookie/đồng ý = ứng viên banner
        const blocks = [...document.querySelectorAll('div,section,aside,dialog,footer,form')].filter(el => { const p = getComputedStyle(el).position; return (p === 'fixed' || p === 'sticky') && vis(el); })
          .map(el => (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 600)).filter(t => RB.test(t) && RC.test(t));
        const links = [...document.querySelectorAll('a[href]')].map(a => ({ t: (a.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 80), h: a.href })).filter(a => RPT.test(a.t) || RPH.test(a.h)).slice(0, 10);
        const body = document.body ? document.body.innerText : '';
        return { banner_blocks: blocks.slice(0, 3), reject_buttons: bt.filter(t => RR.test(t)).slice(0, 5), consent_buttons: bt.filter(t => RC.test(t)).slice(0, 5), policy_links: links,
          lang: document.documentElement.lang || '', title: document.title.slice(0, 200), text_len: body.length, has_password: !!document.querySelector('input[type=password]'),
          bct_badge: !!document.querySelector('a[href*="online.gov.vn"],img[src*="online.gov.vn"],img[src*="dathongbao"],img[src*="bocongthuong"],img[alt*="Bộ Công Thương"],img[alt*="Bộ Công thương"]'),
          press_license: /giấy phép (hoạt động )?(báo|tạp chí|thiết lập trang thông tin)|giấy phép số [^\n]{0,60}(Bộ Thông tin|Cục Báo chí|Bộ Văn hóa|Cục Phát thanh|Sở Thông tin)/i.test(body),
          tax_id: /(mã số (doanh nghiệp|thuế)|MST|giấy chứng nhận (ĐKKD|đăng ký (kinh doanh|doanh nghiệp)))\s*:?\s*\d{10}/i.test(body),
          body_head: body.slice(0, 1500) };
      }, [RE_BANNER.source, RE_CONSENTWORD.source, RE_REJECT.source, RE_POL_TXT.source, RE_POL_HREF.source]);
      Object.assign(rec, info);
      rec.cmp_script = reqs.some(r => RE_CMP.test(r.url));
    }
    if (reject) {
      const loc = page.getByRole('button', { name: RE_REJECT }).or(page.getByText(RE_REJECT));
      const n = await loc.count();
      if (n > 0) {
        try { await loc.first().click({ timeout: 5000 }); clickedAt = Date.now() - t0; rec.reject_clicked_at = clickedAt; rec.reject_click_ok = true; await page.waitForTimeout(WAIT); }
        catch (e) { rec.reject_click_ok = false; rec.reject_click_err = String(e).slice(0, 120); }
      }
      else rec.reject_not_found = true;
    }
    if (detect && shot) await page.screenshot({ path: path.join(OUT, 'shots', s.domain + '.jpg'), type: 'jpeg', quality: 40 }).catch(() => { });
  } catch (e) { rec.ok = false; rec.err = String(e).slice(0, 200); }
  try { rec.cookies = (await ctx.cookies()).map(c => ({ n: c.name, v: c.value.slice(0, 200), d: c.domain, exp: c.expires, http: c.httpOnly, ss: c.sameSite })); } catch { rec.cookies = []; }
  try { rec.storage = await page.evaluate(() => { const o = {}; for (let i = 0; i < Math.min(localStorage.length, 100); i++) { const k = localStorage.key(i); o[k] = (localStorage.getItem(k) || '').slice(0, 200); } return o; }); } catch { rec.storage = {}; }
  rec.requests = reqs; rec.n_requests = reqs.length;
  await ctx.close().catch(() => { });
  return rec;
}

async function fetchPolicy(browser, s, links) {
  // ưu tiên link cùng tên miền, tránh trang chính sách bên thứ ba (Google/Cloudflare/Mozilla/online.gov.vn) và tin tức
  const RE_EXT_VENDOR = /(^|\.)(google\.com|mozilla\.org|cloudflare\.com|microsoft\.com|online\.gov\.vn|cookiesandyou\.com|facebook\.com|apple\.com)$/i;
  const score = l => {
    let u; try { u = new URL(l.h); } catch { return -99; }
    if (!/^https?:$/.test(u.protocol)) return -99;
    const h = u.hostname.toLowerCase(), p = u.pathname.toLowerCase(), t = (l.t || '').trim();
    let sc = 0;
    if (h === s.domain || h.endsWith('.' + s.domain)) sc += 4;
    if (RE_EXT_VENDOR.test(h)) sc -= 10;
    if (/^(chính sách|quyền riêng tư|bảo vệ dữ liệu|điều khoản bảo mật|privacy|cookie policy)/i.test(t) && t.length < 60) sc += 3;
    else if (/(bảo mật|riêng tư|privacy|dữ liệu cá nhân)/i.test(t) && t.length < 60) sc += 2;
    if (/(chinh-sach|privacy|bao-mat|rieng-tu|du-lieu-ca-nhan|cookie)/i.test(p)) sc += 1;
    if (/(tintuc|tin-tuc|chitiet|chi-tiet-tin|\/news\/)/i.test(p) && !/^(chính sách|privacy)/i.test(t)) sc -= 4;
    return sc;
  };
  const cand = links.map(l => ({ ...l, _sc: score(l) })).filter(l => l._sc > 0).sort((a, b) => b._sc - a._sc);
  if (!cand.length) return null;
  const ctx = await browser.newContext({ locale: 'vi-VN', userAgent: UA, ignoreHTTPSErrors: true });
  const page = await ctx.newPage(); let res = null;
  try { await page.goto(cand[0].h, { waitUntil: 'domcontentloaded', timeout: 30000 }); await page.waitForTimeout(3000);
    const txt = await page.evaluate(() => document.body ? document.body.innerText : '');
    fs.writeFileSync(path.join(OUT, 'policy', s.domain + '.txt'), txt);
    res = { policy_url: page.url(), policy_chars: txt.length, policy_link_text: cand[0].t };
  } catch (e) { res = { policy_url: cand[0].h, policy_err: String(e).slice(0, 120) }; }
  await ctx.close().catch(() => { });
  return res;
}

const MINFREE = +(process.env.MIN_FREE_MB || 700) * 1e6;
const RECYCLE = +(process.env.RECYCLE_EVERY || 25), SITE_TIMEOUT = +(process.env.SITE_TIMEOUT_S || 120) * 1000;
const memAvail = () => { try { const m = fs.readFileSync('/proc/meminfo', 'utf8').match(/MemAvailable:\s+(\d+)/); return +m[1] * 1024; } catch { return require('os').freemem(); } };
// Số lần đã thử mỗi site (ghi TRƯỚC khi làm): site làm tiến trình chết ≥ 2 lần thì bỏ, ghi lỗi
const attF = path.join(OUT, 'attempts.txt');
const att = {}; if (fs.existsSync(attF)) for (const d of fs.readFileSync(attF, 'utf8').split('\n').filter(Boolean)) att[d] = (att[d] || 0) + 1;
const launch = () => chromium.launch({ executablePath: process.env.CHROME, headless: true, args: ['--no-first-run', '--disable-blink-features=AutomationControlled', '--disable-dev-shm-usage', '--renderer-process-limit=2', '--js-flags=--max-old-space-size=512'] });
const withTimeout = (p, ms) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error('SITE_TIMEOUT')), ms))]);
async function doSite(browser, s, wid) {
  const A = await visit(browser, s, 'A', { detect: true, shot: !PREPASS });
  if (PREPASS) { delete A.requests; delete A.cookies; delete A.storage; out.write(JSON.stringify(A) + '\n');
    log(`[${wid}] PREPASS ${s.domain} ok=${A.ok} bct=${A.bct_badge} press=${A.press_license} tax=${A.tax_id} lang=${A.lang}`); return A.ok; }
  const Bp = await visit(browser, s, 'B');
  if (A.ok && A.policy_links && A.policy_links.length) Object.assign(A, await fetchPolicy(browser, s, A.policy_links) || {});
  out.write(JSON.stringify(A) + '\n'); out.write(JSON.stringify(Bp) + '\n');
  if (A.ok && A.reject_buttons && A.reject_buttons.length) { const C = await visit(browser, s, 'C', { reject: true }); out.write(JSON.stringify(C) + '\n'); }
  log(`[${wid}] ${s.domain} ${s.stratum} ok=${A.ok} req=${A.n_requests}/${Bp.n_requests} cookies=${(A.cookies || []).length} banner=${(A.banner_blocks || []).length} reject=${(A.reject_buttons || []).length} pol=${A.policy_chars || 0}`);
  return A.ok;
}
async function worker(queue, wid) {
  let browser = null, n = 0;
  while (queue.length) {
    while (memAvail() < MINFREE) { log(`[MEM] ${wid} chờ: RAM khả dụng ${(memAvail() / 1e6).toFixed(0)}MB < ${MINFREE / 1e6}MB`); await new Promise(r => setTimeout(r, 20000)); }
    if (!browser || !browser.isConnected() || n >= RECYCLE) { if (browser) await browser.close().catch(() => { }); log(`[BROWSER] ${wid} khởi động (sau ${n} site)`); browser = await launch(); n = 0; }
    const s = queue.shift(); if (!s) break;  // luồng khác đã lấy site cuối trong lúc mình mở trình duyệt
    if ((att[s.domain] || 0) >= 2) { log(`[SKIP] ${s.domain}: đã làm tiến trình dừng ${att[s.domain]} lần → ghi lỗi`); out.write(JSON.stringify({ domain: s.domain, origin: s.origin, stratum: s.stratum, profile: 'A', ok: false, err: 'CRASHED_TWICE' }) + '\n'); fs.appendFileSync(doneF, s.domain + '\n'); stat.fail++; stat.done++; continue; }
    fs.appendFileSync(attF, s.domain + '\n'); stat.active[s.domain] = 1; n++;
    try {
      const ok = await withTimeout(doSite(browser, s, wid), SITE_TIMEOUT);
      ok ? stat.ok++ : stat.fail++;
    } catch (e) {
      const m = String(e); stat.fail++;
      log('[ERR]', wid, s.domain, m.slice(0, 150));
      out.write(JSON.stringify({ domain: s.domain, origin: s.origin, stratum: s.stratum, profile: 'A', ok: false, err: m.slice(0, 150) }) + '\n');
      await browser.close().catch(() => { }); browser = null;  // đóng hẳn để giết trang treo
    }
    fs.appendFileSync(doneF, s.domain + '\n'); delete stat.active[s.domain]; stat.done++;
  }
  if (browser) await browser.close().catch(() => { });
}

(async () => {
  log(`Bắt đầu: ${sites.length} site (đã xong trước: ${done.size}), par=${PAR}, wait=${WAIT / 1000}s, tái khởi động trình duyệt mỗi ${RECYCLE} site, timeout ${SITE_TIMEOUT / 1000}s/site`);
  const queue = [...sites];
  await Promise.all([...Array(PAR)].map((_, i) => worker(queue, 'w' + i)));
  out.end();
  log(`XONG: ${stat.done} site, ok=${stat.ok}, fail=${stat.fail}, ${Math.round((Date.now() - stat.t0) / 60000)} phút`);
})().catch(e => { log('[FATAL]', e); process.exit(1); });
