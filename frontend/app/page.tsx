"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";

type Track = {
  name: string;
  artist: string;
  album: string;
  spotify_id: string;
};

type Artist = {
  name: string;
  spotify_id: string;
};

const API_BASE = "http://127.0.0.1:8000";
const TIME_RANGES = [
  { value: "short_term", label: "Last 4 Weeks" },
  { value: "medium_term", label: "Last 6 Months" },
  { value: "long_term", label: "All Time" },
] as const;

export default function Home() {
  const [timeRange, setTimeRange] = useState<string>("short_term");
  const [tracks, setTracks] = useState<Track[]>([]);
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    Promise.all([
      fetch(`${API_BASE}/me/top-tracks?time_range=${timeRange}&limit=10`).then((r) => {
        if (!r.ok) throw new Error("Failed to load top tracks");
        return r.json();
      }),
      fetch(`${API_BASE}/me/top-artists?time_range=${timeRange}&limit=10`).then((r) => {
        if (!r.ok) throw new Error("Failed to load top artists");
        return r.json();
      }),
    ])
      .then(([trackData, artistData]) => {
        setTracks(trackData.tracks);
        setArtists(artistData.artists);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [timeRange]);

  return (
    <main className="min-h-screen bg-[#0A0A0B] text-[#F2F0EA] px-6 py-16 md:px-16">
      <div className="mx-auto max-w-3xl">
        <header className="mb-12">
          <p className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-3">
            Listening Report
          </p>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-4">
            Your Top Sounds
          </h1>
          <Link
            href="/trends"
            className="font-mono text-sm text-[#8A8680] hover:text-[#B8434F] transition-colors"
          >
            View Trends →
          </Link>
        </header>

        <Tabs value={timeRange} onValueChange={setTimeRange} className="mb-10">
          <TabsList className="bg-transparent border-b border-[#8A8680]/20 rounded-none w-full justify-start gap-6 p-0">
            {TIME_RANGES.map((range) => (
              <TabsTrigger
                key={range.value}
                value={range.value}
                className="font-mono text-sm uppercase tracking-wide rounded-none border-b-2 border-transparent data-[state=active]:border-[#8C2F39] data-[state=active]:text-[#F2F0EA] text-[#8A8680] bg-transparent px-1 pb-3 shadow-none"
              >
                {range.label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>

        {error && (
          <p className="font-mono text-sm text-[#B8434F] mb-8">
            {error} — is your backend running at {API_BASE}?
          </p>
        )}

        <section className="mb-16">
          <h2 className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-6">
            Top Tracks
          </h2>
          <ol className="divide-y divide-[#8A8680]/10">
            {loading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <li key={i} className="flex items-center gap-4 py-4">
                    <Skeleton className="h-6 w-6 bg-[#8A8680]/10" />
                    <Skeleton className="h-5 flex-1 bg-[#8A8680]/10" />
                  </li>
                ))
              : tracks.map((track, i) => (
                  <li key={track.spotify_id} className="flex items-baseline gap-4 py-4">
                    <span className="font-mono text-sm text-[#8C2F39] w-6 shrink-0">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <div className="min-w-0">
                      <p className="text-lg font-semibold truncate">{track.name}</p>
                      <p className="text-sm text-[#8A8680] truncate">
                        {track.artist} · {track.album}
                      </p>
                    </div>
                  </li>
                ))}
          </ol>
        </section>

        <section>
          <h2 className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-6">
            Top Artists
          </h2>
          <ol className="divide-y divide-[#8A8680]/10">
            {loading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <li key={i} className="flex items-center gap-4 py-4">
                    <Skeleton className="h-6 w-6 bg-[#8A8680]/10" />
                    <Skeleton className="h-5 flex-1 bg-[#8A8680]/10" />
                  </li>
                ))
              : artists.map((artist, i) => (
                  <li key={artist.spotify_id} className="flex items-baseline gap-4 py-4">
                    <span className="font-mono text-sm text-[#8C2F39] w-6 shrink-0">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <p className="text-lg font-semibold truncate">{artist.name}</p>
                  </li>
                ))}
          </ol>
        </section>
      </div>
    </main>
  );
}
