import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { BookOpen, ExternalLink, Play, Filter, Sparkles } from 'lucide-react';
import { resourcesApi } from '../../api/resources';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import Loader from '../../components/common/Loader';

const WEAK_AREA_TAGS = [
  { id: 'all', label: 'All Resources' },
  { id: 'eye_contact', label: 'Eye Contact' },
  { id: 'body_language', label: 'Body Language & Posture' },
  { id: 'star_method', label: 'STAR Method' },
  { id: 'filler_words', label: 'Eliminating Fillers' },
  { id: 'confidence', label: 'Confidence & Anxiety' },
  { id: 'english_pronunciation', label: 'Pronunciation & Cadence' },
  { id: 'grammar', label: 'Professional Grammar' },
  { id: 'technical', label: 'System Design & Technical' },
];

export default function ResourcesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialTag = searchParams.get('weak_area') || 'all';

  const [activeTag, setActiveTag] = useState(initialTag);
  const [resources, setResources] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchResources(activeTag);
  }, [activeTag]);

  const fetchResources = async (tag) => {
    setIsLoading(true);
    try {
      const res = await resourcesApi.getResources(tag === 'all' ? '' : tag);
      setResources(res.data);
    } catch (err) {
      // Seeded fallback
      setResources([
        {
          id: 'res-1',
          title: 'How to Maintain Good Eye Contact in Virtual and In-Person Interviews',
          url: 'https://www.youtube.com/watch?v=3mJ7k0d1aJk',
          platform: 'youtube',
          weak_area_tag: 'eye_contact',
          difficulty: 'All',
        },
        {
          id: 'res-2',
          title: 'Your Body Language May Shape Who You Are | Amy Cuddy | TED',
          url: 'https://www.youtube.com/watch?v=Ks-_Mh1QhMc',
          platform: 'youtube',
          weak_area_tag: 'body_language',
          difficulty: 'All',
        },
        {
          id: 'res-3',
          title: 'Master the STAR Method for Behavioral Interview Questions',
          url: 'https://www.youtube.com/watch?v=uG36dZp5j7g',
          platform: 'youtube',
          weak_area_tag: 'star_method',
          difficulty: 'Intermediate',
        },
        {
          id: 'res-4',
          title: "How to Stop Saying 'Um', 'Uh', and 'Like' When You Speak",
          url: 'https://www.youtube.com/watch?v=p1t3F4p1A8c',
          platform: 'youtube',
          weak_area_tag: 'filler_words',
          difficulty: 'All',
        },
        {
          id: 'res-5',
          title: 'How to Build Unshakeable Interview Confidence | Stanford GSB',
          url: 'https://www.youtube.com/watch?v=HAnw168huqA',
          platform: 'youtube',
          weak_area_tag: 'confidence',
          difficulty: 'All',
        },
        {
          id: 'res-6',
          title: 'System Design Interview: Step by Step Guide for Software Engineers',
          url: 'https://www.youtube.com/watch?v=i7twT3x5yv8',
          platform: 'youtube',
          weak_area_tag: 'technical',
          difficulty: 'Advanced',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectTag = (tagId) => {
    setActiveTag(tagId);
    if (tagId === 'all') {
      setSearchParams({});
    } else {
      setSearchParams({ weak_area: tagId });
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          Curated Learning Resources
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Master interview communication, body language, and technical storytelling with vetted tutorials.
        </p>
      </div>

      {/* Weak Area Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {WEAK_AREA_TAGS.map((tag) => (
          <button
            key={tag.id}
            onClick={() => handleSelectTag(tag.id)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              activeTag === tag.id
                ? 'bg-primary-600 text-white shadow-sm'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            {tag.label}
          </button>
        ))}
      </div>

      {/* Resources Grid */}
      {isLoading ? (
        <Loader text="Loading video tutorials..." size="md" />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resources.map((res) => (
            <Card
              key={res.id}
              hoverEffect
              className="border-slate-200 dark:border-slate-800 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="primary" size="sm">
                    {res.weak_area_tag}
                  </Badge>
                  <span className="text-[10px] text-slate-400 uppercase font-mono">
                    {res.difficulty}
                  </span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white leading-snug">
                  {res.title}
                </h3>
              </div>

              <div className="pt-6 mt-4 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between">
                <span className="text-xs text-slate-500 capitalize">{res.platform}</span>
                <a
                  href={res.url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-primary-500 hover:text-primary-400"
                >
                  <Play className="w-3.5 h-3.5" />
                  Watch Video &rarr;
                </a>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
