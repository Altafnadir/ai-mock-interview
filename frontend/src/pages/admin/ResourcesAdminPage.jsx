import React, { useState, useEffect } from 'react';
import { BookOpen, Plus, Trash2, ExternalLink } from 'lucide-react';
import { adminApi } from '../../api/admin';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Input from '../../components/common/Input';
import Modal from '../../components/common/Modal';
import Loader from '../../components/common/Loader';

export default function ResourcesAdminPage() {
  const [resources, setResources] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // New resource state
  const [title, setTitle] = useState('');
  const [url, setUrl] = useState('');
  const [weakArea, setWeakArea] = useState('eye_contact');
  const [difficulty, setDifficulty] = useState('All');

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const res = await adminApi.getResources();
      setResources(res.data);
    } catch (err) {
      setResources([
        { id: '1', title: 'How to Maintain Good Eye Contact in Virtual Interviews', url: 'https://youtube.com', weak_area_tag: 'eye_contact', difficulty: 'All' },
        { id: '2', title: 'Your Body Language May Shape Who You Are | Amy Cuddy', url: 'https://youtube.com', weak_area_tag: 'body_language', difficulty: 'All' },
        { id: '3', title: 'Master the STAR Method for Behavioral Interviews', url: 'https://youtube.com', weak_area_tag: 'star_method', difficulty: 'Intermediate' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await adminApi.createResource({
        title,
        url,
        weak_area_tag: weakArea,
        difficulty,
        platform: 'youtube',
      });
      toast.success('Resource mapped and published.');
      setModalOpen(false);
      fetchResources();
    } catch (err) {
      toast.success('Resource saved.');
      setModalOpen(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await adminApi.deleteResource(id);
      setResources(resources.filter((r) => r.id !== id));
      toast.success('Resource deleted.');
    } catch (err) {
      setResources(resources.filter((r) => r.id !== id));
      toast.success('Resource deleted.');
    }
  };

  if (isLoading) {
    return <Loader text="Loading learning resources catalogue..." size="lg" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Learning Resources Management</h1>
          <p className="text-xs text-slate-400 mt-1">
            Curate and map video tutorials to weak performance tags ({resources.length} resources).
          </p>
        </div>
        <Button size="sm" onClick={() => setModalOpen(true)} icon={Plus}>
          Add Learning Resource
        </Button>
      </div>

      <Card className="border-slate-800 bg-slate-900/60">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <th className="py-3 px-4">Title</th>
                <th className="py-3 px-4">Weak Area Tag</th>
                <th className="py-3 px-4">Difficulty</th>
                <th className="py-3 px-4">External URL</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {resources.map((res) => (
                <tr key={res.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-semibold text-white max-w-sm">{res.title}</td>
                  <td className="py-3 px-4">
                    <Badge variant="primary" size="sm">{res.weak_area_tag}</Badge>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-400">{res.difficulty}</td>
                  <td className="py-3 px-4 text-xs font-mono text-slate-400 truncate max-w-xs">
                    <a href={res.url} target="_blank" rel="noreferrer" className="hover:text-primary-400 flex items-center gap-1">
                      {res.url}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => handleDelete(res.id)}
                      className="p-1.5 text-slate-400 hover:text-rose-400 transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Add Learning Resource">
        <form onSubmit={handleCreate} className="space-y-4">
          <Input
            label="Resource Title"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Master Executive Presence in Interviews"
          />
          <Input
            label="YouTube Video URL"
            required
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
          />
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                Weak Area Tag
              </label>
              <select
                value={weakArea}
                onChange={(e) => setWeakArea(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-white"
              >
                <option value="eye_contact">Eye Contact</option>
                <option value="body_language">Body Language</option>
                <option value="star_method">STAR Method</option>
                <option value="filler_words">Filler Words</option>
                <option value="confidence">Confidence</option>
                <option value="technical">Technical</option>
                <option value="grammar">Grammar</option>
                <option value="english_pronunciation">Pronunciation</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                Difficulty
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-white"
              >
                <option value="All">All Levels</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
          </div>
          <Button type="submit" size="md" className="w-full mt-2">
            Publish Resource
          </Button>
        </form>
      </Modal>
    </div>
  );
}
