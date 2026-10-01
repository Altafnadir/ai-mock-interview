import React, { useState, useEffect } from 'react';
import { User, Mail, Phone, Plus, X, Save, Upload, Briefcase, GraduationCap, Award } from 'lucide-react';
import { profileApi } from '../../api/profile';
import { useAuthStore } from '../../store/authStore';
import { toast } from '../../store/toastStore';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Badge from '../../components/common/Badge';
import Loader from '../../components/common/Loader';

const AVAILABLE_ROLES = [
  'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
  'Software Engineer', 'QA Engineer', 'Data Analyst',
  'Cybersecurity Analyst', 'Mobile App Developer', 'DevOps Engineer',
  'AI/ML Engineer', 'Business Analyst'
];

export default function ProfilePage() {
  const { user, updateUser } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  // Form State
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [phone, setPhone] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('beginner');
  const [preferredRoles, setPreferredRoles] = useState([]);
  const [skills, setSkills] = useState([]);
  const [newSkill, setNewSkill] = useState('');
  const [education, setEducation] = useState([]);
  const [workExperience, setWorkExperience] = useState([]);
  const [certifications, setCertifications] = useState([]);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await profileApi.getProfile();
      const p = res.data;
      setPhone(p.phone || '');
      setExperienceLevel(p.experience_level || 'beginner');
      setPreferredRoles(p.preferred_job_roles || []);
      setSkills(p.skills || []);
      setEducation(p.education || []);
      setWorkExperience(p.work_experience || []);
      setCertifications(p.certifications || []);
    } catch (err) {
      // Defaults from seeded demo candidate
      setPhone('+92 300 1234567');
      setExperienceLevel('beginner');
      setPreferredRoles(['Frontend Developer', 'Full Stack Developer']);
      setSkills(['React.js', 'JavaScript', 'Python', 'FastAPI', 'SQL', 'Tailwind CSS', 'Git', 'Docker']);
      setEducation([
        { degree: 'BS Software Engineering', institution: 'PMAS-Arid Agriculture University (GIMS)', year: '2024', gpa: '3.75' }
      ]);
      setWorkExperience([
        { role: 'Frontend Intern', company: 'TechSolutions Islamabad', duration: '6 months', highlights: 'Built responsive React dashboards.' }
      ]);
      setCertifications([
        { title: 'Meta Frontend Developer Professional Certificate', issuer: 'Coursera', year: '2023' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddSkill = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const val = newSkill.trim().replace(',', '');
      if (val && !skills.includes(val)) {
        setSkills([...skills, val]);
        setNewSkill('');
      }
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  const togglePreferredRole = (role) => {
    if (preferredRoles.includes(role)) {
      setPreferredRoles(preferredRoles.filter((r) => r !== role));
    } else {
      setPreferredRoles([...preferredRoles, role]);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await profileApi.updateProfile({
        full_name: fullName,
        phone,
        experience_level: experienceLevel,
        preferred_job_roles: preferredRoles,
        skills,
        education,
        work_experience: workExperience,
        certifications,
      });

      updateUser({ ...user, full_name: fullName });
      toast.success('Candidate profile updated successfully!');
    } catch (err) {
      toast.error('Failed to update profile.');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <Loader text="Loading your profile data..." size="lg" />;
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Candidate Profile</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Personalize your background and target tech roles for tailored interview questions.
          </p>
        </div>
        <Button onClick={handleSave} isLoading={isSaving} icon={Save}>
          Save Profile
        </Button>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* Personal Details */}
        <Card title="Personal Information" className="border-slate-200 dark:border-slate-800">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Full Name"
              icon={User}
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
            <Input
              label="Email Address"
              icon={Mail}
              disabled
              value={user?.email || ''}
              helperText="Verified account email"
            />
            <Input
              label="Phone Number"
              icon={Phone}
              placeholder="+92 300 1234567"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                Experience Level
              </label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-sm text-slate-900 dark:text-slate-100 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
              >
                <option value="beginner">Beginner (0-2 years, Fresh Graduate)</option>
                <option value="intermediate">Intermediate (2-5 years experience)</option>
                <option value="advanced">Advanced (5+ years senior/lead)</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Preferred Job Roles */}
        <Card title="Target Job Roles" subtitle="Select the positions you are actively interviewing for" className="border-slate-200 dark:border-slate-800">
          <div className="flex flex-wrap gap-2 pt-2">
            {AVAILABLE_ROLES.map((role) => {
              const selected = preferredRoles.includes(role);
              return (
                <button
                  key={role}
                  type="button"
                  onClick={() => togglePreferredRole(role)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selected
                      ? 'bg-primary-600 text-white shadow-sm font-semibold'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {role} {selected && '✓'}
                </button>
              );
            })}
          </div>
        </Card>

        {/* Technical Skills Tag Input */}
        <Card title="Technical Skills" subtitle="Press Enter or Comma to add new skills to your profile" className="border-slate-200 dark:border-slate-800">
          <div className="space-y-3">
            <Input
              placeholder="e.g. Docker, TypeScript, PyTorch, GraphQL..."
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              onKeyDown={handleAddSkill}
            />
            <div className="flex flex-wrap gap-2 pt-1">
              {skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-primary-100 dark:bg-primary-950/80 text-primary-700 dark:text-primary-300 border border-primary-200 dark:border-primary-800"
                >
                  {skill}
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(skill)}
                    className="hover:text-rose-500 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        </Card>

        {/* Education & Work Experience Summaries */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card title="Education" className="border-slate-200 dark:border-slate-800">
            <div className="space-y-3">
              {education.map((edu, idx) => (
                <div key={idx} className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <div className="flex items-center gap-2 font-semibold text-sm text-slate-800 dark:text-slate-200">
                    <GraduationCap className="w-4 h-4 text-primary-500" />
                    {edu.degree}
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{edu.institution} &bull; Class of {edu.year}</p>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Experience & Internships" className="border-slate-200 dark:border-slate-800">
            <div className="space-y-3">
              {workExperience.map((exp, idx) => (
                <div key={idx} className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <div className="flex items-center gap-2 font-semibold text-sm text-slate-800 dark:text-slate-200">
                    <Briefcase className="w-4 h-4 text-primary-500" />
                    {exp.role}
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{exp.company} &bull; {exp.duration}</p>
                  <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 italic">{exp.highlights}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </form>
    </div>
  );
}
