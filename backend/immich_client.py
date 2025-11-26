import httpx
import asyncio

class ImmichClient:
    def __init__(self, base_url, api_key):
        self.base = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key}

    async def get_unreviewed(self, limit=1):
        # use the random endpoint which works with this Immich version
        # fetch multiple in parallel if limit > 1
        if limit == 1:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{self.base}/assets/random",
                    headers=self.headers,
                    timeout=10.0,
                )
            r.raise_for_status()
            data = r.json()
            # random endpoint returns a single asset or list
            if isinstance(data, list):
                return data[:limit]
            else:
                return [data]  # wrap single asset in list
        else:
            # Fetch multiple random assets in parallel
            async with httpx.AsyncClient() as client:
                tasks = [
                    client.get(
                        f"{self.base}/assets/random",
                        headers=self.headers,
                        timeout=10.0,
                    )
                    for _ in range(limit)
                ]
                responses = await asyncio.gather(*tasks)
            
            assets = []
            seen_ids = set()
            for r in responses:
                r.raise_for_status()
                data = r.json()
                asset = data if isinstance(data, dict) else data[0] if isinstance(data, list) else None
                if asset and asset.get("id") not in seen_ids:
                    assets.append(asset)
                    seen_ids.add(asset["id"])
            
            return assets

    async def mark_favorite(self, asset_id, favorite=True):
        async with httpx.AsyncClient() as client:
            r = await client.put(
                f"{self.base}/assets",
                json={"ids": [asset_id], "isFavorite": favorite},
                headers=self.headers,
            )
        return r.json()

    async def archive(self, asset_id, archived=True):
        async with httpx.AsyncClient() as client:
            r = await client.put(
                f"{self.base}/assets",
                json={"ids": [asset_id], "isArchived": archived},
                headers=self.headers,
            )
        return r.json()

    async def delete(self, asset_id):
        async with httpx.AsyncClient() as client:
            r = await client.request(
                "DELETE",
                f"{self.base}/assets",
                json={"ids": [asset_id]},
                headers=self.headers,
            )
        return r.json()

    async def restore(self, asset_id):
        """Restore asset from trash"""
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.base}/trash/restore/assets",
                json={"ids": [asset_id]},
                headers=self.headers,
            )
        return r.json()
