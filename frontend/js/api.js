/* ==========================================================================
   API Helper — GOS Chemicals
   Shared fetch wrappers used by all page-specific JS files.
   Includes in-memory + sessionStorage caching to eliminate duplicate
   network requests and provide instant sub-page transitions.
   ========================================================================== */

const API_BASE = '/api';
const _apiCache = {};
const CACHE_TTL_MS = 15 * 60 * 1000; // 15 minutes

function apiGetCachedSync(path) {
    try {
        const stored = sessionStorage.getItem(`gos_api_${path}`);
        if (stored) {
            const { timestamp, data } = JSON.parse(stored);
            if (Date.now() - timestamp < CACHE_TTL_MS) {
                return data;
            }
        }
    } catch (e) {}
    return null;
}

async function apiGet(path) {
    if (_apiCache[path]) return _apiCache[path];

    // Check sessionStorage cache for instant response
    const cachedData = apiGetCachedSync(path);
    if (cachedData !== null) {
        _apiCache[path] = Promise.resolve(cachedData);
        return cachedData;
    }

    const promise = fetch(`${API_BASE}${path}`)
        .then(res => {
            if (!res.ok) throw new Error(`API error: ${res.status}`);
            return res.json();
        })
        .then(data => {
            try {
                sessionStorage.setItem(`gos_api_${path}`, JSON.stringify({
                    timestamp: Date.now(),
                    data
                }));
            } catch (e) {}
            return data;
        });

    _apiCache[path] = promise;
    return promise;
}

async function apiPost(path, data) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    return res.json();
}
