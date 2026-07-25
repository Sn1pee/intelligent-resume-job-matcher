document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const resumeFileInput = document.getElementById('resumeFileInput');
    const fileSelectedBanner = document.getElementById('fileSelectedBanner');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const fileSizeDisplay = document.getElementById('fileSizeDisplay');
    const removeFileBtn = document.getElementById('removeFileBtn');

    const jobDescriptionInput = document.getElementById('jobDescriptionInput');
    const charCountDisplay = document.getElementById('charCountDisplay');
    const wordCountDisplay = document.getElementById('wordCountDisplay');

    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');

    const loadSampleBtn = document.getElementById('loadSampleBtn');
    const resultsDashboard = document.getElementById('resultsDashboard');

    // State Variables
    let selectedFile = null;

    // --- File Drag & Drop Handlers ---
    dropzone.addEventListener('click', () => resumeFileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dropzone-active');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dropzone-active');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dropzone-active');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    resumeFileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearSelectedFile();
    });

    function handleFileSelect(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showError('Please select a valid PDF resume file (.pdf).');
            return;
        }
        hideError();
        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        fileSizeDisplay.textContent = formatBytes(file.size);
        fileSelectedBanner.classList.remove('hidden');
        fileSelectedBanner.classList.add('flex');
    }

    function clearSelectedFile() {
        selectedFile = null;
        resumeFileInput.value = '';
        fileSelectedBanner.classList.add('hidden');
        fileSelectedBanner.classList.remove('flex');
    }

    // --- Job Description Counter ---
    jobDescriptionInput.addEventListener('input', () => {
        const text = jobDescriptionInput.value;
        charCountDisplay.textContent = `${text.length} characters`;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        wordCountDisplay.textContent = `${words} words`;
    });

    // --- Load Sample Data Handler ---
    loadSampleBtn.addEventListener('click', async () => {
        hideError();
        // Set sample job description text
        jobDescriptionInput.value = `Data Analyst & Python Developer

Key Responsibilities:
- Build data processing pipelines using Python, Pandas, and NumPy.
- Write complex SQL queries to extract data from PostgreSQL and MySQL.
- Develop interactive dashboards using Power BI and Tableau.
- Perform exploratory data analysis using Scikit-learn.
- Collaborate with engineering teams to deploy REST APIs using FastAPI or Flask.
- Utilize Git and GitHub for version control.

Requirements:
- Bachelor's degree in Computer Science or related field.
- 1+ years experience with Python, SQL, Pandas, NumPy, and Git.
- Experience with Power BI or Tableau.`;

        jobDescriptionInput.dispatchEvent(new Event('input'));

        // Generate synthetic sample PDF file in memory for instant demo
        const samplePdfContent = "%PDF-1.4 sample resume content placeholder";
        const blob = new Blob([samplePdfContent], { type: 'application/pdf' });
        const sampleFile = new File([blob], "sample_resume.pdf", { type: "application/pdf" });

        // Fetch real sample resume PDF from sample endpoint if available, or fetch sample_resume.pdf
        try {
            // Check if we can fetch real sample_data/sample_resume.pdf from server
            const res = await fetch('/static/sample_data/sample_resume.pdf');
            if (res.ok) {
                const fetchedBlob = await res.blob();
                const file = new File([fetchedBlob], "sample_resume.pdf", { type: "application/pdf" });
                handleFileSelect(file);
            } else {
                handleFileSelect(sampleFile);
            }
        } catch (e) {
            handleFileSelect(sampleFile);
        }
    });

    // --- Submit Form Analysis ---
    analyzeBtn.addEventListener('click', async () => {
        hideError();

        const jobDescriptionText = jobDescriptionInput.value.trim();

        if (!selectedFile) {
            showError('Please upload your resume in PDF format before analyzing.');
            return;
        }

        if (!jobDescriptionText) {
            showError('Please paste a job description into the text area.');
            return;
        }

        // Set Loading UI State
        setLoadingState(true);

        const formData = new FormData();
        formData.append('resume_file', selectedFile);
        formData.append('job_description', jobDescriptionText);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to analyze resume. Please try again.');
            }

            // Render Analysis Results
            renderResults(data);

        } catch (err) {
            showError(err.message || 'An unexpected error occurred while connecting to the server.');
        } finally {
            setLoadingState(false);
        }
    });

    // --- Render Results Dashboard ---
    function renderResults(data) {
        const { overall_score, match_category, category_color, breakdown, skills, insights, metadata } = data;

        // Display metadata
        const metaText = `Analyzed ${metadata.resume_filename} (${metadata.page_count} page${metadata.page_count > 1 ? 's' : ''}) against job description (${metadata.job_character_count} chars)`;
        document.getElementById('analysisMetaDisplay').textContent = metaText;
        document.getElementById('methodBadge').textContent = breakdown.similarity_method;

        // 1. Overall Score Ring Animation
        const scoreRing = document.getElementById('scoreRing');
        const circumference = 314.15; // 2 * PI * 50
        const strokeOffset = circumference - (circumference * overall_score / 100);
        
        scoreRing.style.strokeDashoffset = strokeOffset;
        
        // Color mapping for score ring
        let ringColorClass = "stroke-emerald-500";
        let badgeBgClass = "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";

        if (overall_score < 40) {
            ringColorClass = "stroke-rose-500";
            badgeBgClass = "bg-rose-500/10 text-rose-400 border-rose-500/30";
        } else if (overall_score < 60) {
            ringColorClass = "stroke-amber-500";
            badgeBgClass = "bg-amber-500/10 text-amber-400 border-amber-500/30";
        } else if (overall_score < 80) {
            ringColorClass = "stroke-blue-500";
            badgeBgClass = "bg-blue-500/10 text-blue-400 border-blue-500/30";
        }

        scoreRing.className = `transition-all duration-1000 ease-out ${ringColorClass}`;
        
        // Score number counter animation
        animateValue(document.getElementById('scorePercentageDisplay'), 0, overall_score, 1000, '%');

        const categoryBadge = document.getElementById('scoreCategoryBadge');
        categoryBadge.textContent = match_category;
        categoryBadge.className = `mt-1 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${badgeBgClass}`;

        // 2. Score Component Bars
        document.getElementById('skillScoreValue').textContent = `${breakdown.skill_match_score}%`;
        document.getElementById('skillScoreBar').style.width = `${breakdown.skill_match_score}%`;

        document.getElementById('similarityScoreValue').textContent = `${breakdown.semantic_similarity_score}%`;
        document.getElementById('similarityScoreBar').style.width = `${breakdown.semantic_similarity_score}%`;

        document.getElementById('relevanceScoreValue').textContent = `${breakdown.relevance_score}%`;
        document.getElementById('relevanceScoreBar').style.width = `${breakdown.relevance_score}%`;

        // 3. Render Skill Badges
        renderSkillBadges('matchingSkillsContainer', 'matchingSkillsCount', skills.matching_skills, 'badge-match', 'fa-circle-check');
        renderSkillBadges('missingSkillsContainer', 'missingSkillsCount', skills.missing_skills, 'badge-missing', 'fa-circle-xmark');
        renderSkillBadges('additionalSkillsContainer', 'additionalSkillsCount', skills.additional_skills, 'badge-additional', 'fa-circle-plus');

        // 4. Render Insights Lists
        renderList('strengthsList', insights.strengths, 'fa-check text-emerald-400');
        renderList('improvementsList', insights.improvements, 'fa-arrow-right text-amber-400');
        renderList('recommendationsList', insights.recommended_skills, 'fa-bullseye text-indigo-400');

        // Unhide Dashboard & Scroll smoothly into view
        resultsDashboard.classList.remove('hidden');
        resultsDashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderSkillBadges(containerId, countId, skillList, badgeClass, iconClass) {
        const container = document.getElementById(containerId);
        const countSpan = document.getElementById(countId);
        
        countSpan.textContent = skillList.length;
        container.innerHTML = '';

        if (!skillList || skillList.length === 0) {
            container.innerHTML = `<span class="text-xs text-slate-500 italic">None detected</span>`;
            return;
        }

        skillList.forEach(skill => {
            const badge = document.createElement('span');
            badge.className = `badge-skill ${badgeClass}`;
            badge.innerHTML = `<i class="fa-solid ${iconClass}"></i> ${escapeHtml(skill)}`;
            container.appendChild(badge);
        });
    }

    function renderList(listId, items, iconClasses) {
        const ul = document.getElementById(listId);
        ul.innerHTML = '';

        if (!items || items.length === 0) {
            ul.innerHTML = `<li class="text-xs text-slate-500 italic">No specific items generated.</li>`;
            return;
        }

        items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'flex items-start gap-2.5';
            li.innerHTML = `
                <i class="fa-solid ${iconClasses} mt-1 shrink-0"></i>
                <span class="leading-relaxed">${escapeHtml(item)}</span>
            `;
            ul.appendChild(li);
        });
    }

    // --- Helper Functions ---
    function setLoadingState(isLoading) {
        analyzeBtn.disabled = isLoading;
        if (isLoading) {
            btnText.classList.add('hidden');
            btnSpinner.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            btnSpinner.classList.add('hidden');
        }
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorAlert.classList.remove('hidden');
    }

    function hideError() {
        errorAlert.classList.add('hidden');
    }

    function formatBytes(bytes, decimals = 1) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    function animateValue(obj, start, end, duration, suffix = '') {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentVal = (progress * (end - start) + start).toFixed(1);
            obj.textContent = `${currentVal}${suffix}`;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
