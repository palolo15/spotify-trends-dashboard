"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type VolumePoint = { date: string; play_count: number };
type TurnoverWeek = {
  week: string;
  total_unique_artists: number;
  new_artists: string[];
  new_artist_count: number;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export default function TrendsPage() {
  const [volume, setVolume] = useState<VolumePoint[]>([]);
  const [turnover, setTurnover] = useState<TurnoverWeek[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/trends/volume`).then((r) => {
        if (!r.ok) throw new Error("Failed to load volume trends");
        return r.json();
      }),
      fetch(`${API_BASE}/trends/artist-turnover`).then((r) => {
        if (!r.ok) throw new Error("Failed to load artist turnover");
        return r.json();
      }),
    ])
      .then(([volumeData, turnoverData]) => {
        setVolume(volumeData.data);
        setTurnover(turnoverData.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const isSparse = volume.length < 5;

  return (
    <main className="min-h-screen bg-[#0A0A0B] text-[#F2F0EA] px-6 py-16 md:px-16">
      <div className="mx-auto max-w-3xl">
        <header className="mb-4">
          <p className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-3">
            Listening Report
          </p>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-4">
            Trends Over Time
          </h1>
          <Link
            href="/"
            className="font-mono text-sm text-[#8A8680] hover:text-[#B8434F] transition-colors"
          >
            ← Back to Top Sounds
          </Link>
        </header>

        {error && (
          <p className="font-mono text-sm text-[#B8434F] mt-8">
            {error} — is your backend running at {API_BASE}?
          </p>
        )}

        {!loading && !error && isSparse && (
          <p className="font-mono text-sm text-[#8A8680] mt-10 mb-6 border border-[#8A8680]/20 px-4 py-3">
            Still collecting data — trends get more interesting the longer the
            snapshot job runs. Check back after a few more days of listening.
          </p>
        )}

        <section className="mt-12 mb-16">
          <h2 className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-6">
            Listening Volume
          </h2>
          {loading ? (
            <div className="h-64 bg-[#8A8680]/5 animate-pulse" />
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={volume}>
                <CartesianGrid strokeDasharray="3 3" stroke="#8A868020" />
                <XAxis
                  dataKey="date"
                  stroke="#8A8680"
                  fontSize={12}
                  fontFamily="monospace"
                />
                <YAxis stroke="#8A8680" fontSize={12} fontFamily="monospace" />
                <Tooltip
                  contentStyle={{
                    background: "#0A0A0B",
                    border: "1px solid #8A868040",
                    fontFamily: "monospace",
                    fontSize: 12,
                  }}
                  labelStyle={{ color: "#F2F0EA" }}
                />
                <Bar dataKey="play_count" fill="#8C2F39" radius={[2, 2, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </section>

        <section>
          <h2 className="font-mono text-xs tracking-[0.2em] text-[#8A8680] uppercase mb-6">
            Artist Turnover
          </h2>
          {loading ? (
            <div className="h-40 bg-[#8A8680]/5 animate-pulse" />
          ) : (
            <ol className="divide-y divide-[#8A8680]/10">
              {turnover.map((week) => (
                <li key={week.week} className="py-4">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="font-mono text-sm text-[#F2F0EA]">
                      Week of {week.week}
                    </span>
                    <span className="font-mono text-xs text-[#8A8680]">
                      {week.total_unique_artists} unique ·{" "}
                      <span className="text-[#B8434F]">
                        {week.new_artist_count} new
                      </span>
                    </span>
                  </div>
                  {week.new_artist_count > 0 && (
                    <p className="text-sm text-[#8A8680] truncate">
                      {week.new_artists.slice(0, 6).join(", ")}
                      {week.new_artists.length > 6 &&
                        ` +${week.new_artists.length - 6} more`}
                    </p>
                  )}
                </li>
              ))}
            </ol>
          )}
        </section>
      </div>
    </main>
  );
}