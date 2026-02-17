// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Generate unique user ID
function getUserId() {
    let userId = localStorage.getItem('userId');
    if (!userId) {
        userId = 'U' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userId', userId);
    }
    return userId;
}

// Character Counter
const postTextarea = document.getElementById('postText');
if (postTextarea) {
    const charCount = document.getElementById('charCount');
    
    postTextarea.addEventListener('input', () => {
        const count = postTextarea.value.length;
        charCount.textContent = count;
    });
}

// Analysis Form Submission
const analysisForm = document.getElementById('analysisForm');
if (analysisForm) {
    analysisForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const postText = document.getElementById('postText').value.trim();
        
        if (!postText) {
            showError('Please enter post content');
            return;
        }

        // Show loading state
        const predictBtn = document.getElementById('predictBtn');
        const btnText = predictBtn.querySelector('.btn-text');
        const btnLoader = predictBtn.querySelector('.btn-loader');
        
        predictBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        
        // Hide previous results and errors
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('errorMessage').style.display = 'none';

        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: getUserId(),
                    post_text: postText
                })
            });

            if (!response.ok) {
                throw new Error('Failed to get prediction');
            }

            const data = await response.json();
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            showError('Unable to connect to the server. Please ensure the backend is running.');
        } finally {
            // Reset button state
            predictBtn.disabled = false;
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
        }
    });
}

// Display Results
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    
    // Engagement Level
    const engagementLevel = document.getElementById('engagementLevel');
    const engagementBadge = document.getElementById('engagementBadge');
    
    engagementLevel.textContent = data.engagement_level;
    engagementLevel.className = 'engagement-level';
    
    // Add appropriate class based on level
    if (data.engagement_level === 'High') {
        engagementLevel.classList.add('engagement-high');
    } else if (data.engagement_level === 'Medium') {
        engagementLevel.classList.add('engagement-medium');
    } else {
        engagementLevel.classList.add('engagement-low');
    }
    
    // Confidence Score
    const confidenceScore = document.getElementById('confidenceScore');
    confidenceScore.textContent = (data.confidence_score * 100).toFixed(1) + '%';
    
    // Key Factors with animation
    const keyFactors = document.getElementById('keyFactors');
    keyFactors.innerHTML = '';
    
    if (data.key_factors && Object.keys(data.key_factors).length > 0) {
        let delay = 0;
        for (const [factor, value] of Object.entries(data.key_factors)) {
            const factorItem = document.createElement('div');
            factorItem.className = 'factor-item stagger-item';
            factorItem.style.animationDelay = `${delay}s`;
            
            const factorName = document.createElement('span');
            factorName.className = 'factor-name';
            factorName.textContent = factor.replace(/_/g, ' ');
            
            const factorValue = document.createElement('span');
            factorValue.className = 'factor-value';
            factorValue.textContent = value >= 0 ? `+${value.toFixed(2)}` : value.toFixed(2);
            factorValue.classList.add(value >= 0 ? 'factor-positive' : 'factor-negative');
            
            factorItem.appendChild(factorName);
            factorItem.appendChild(factorValue);
            keyFactors.appendChild(factorItem);
            
            delay += 0.1;
        }
    } else {
        keyFactors.innerHTML = '<p style="color: #6b7280;">No specific factors identified</p>';
    }
    
    // Suggestions with animation
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    
    if (data.suggestions && data.suggestions.length > 0) {
        data.suggestions.forEach((suggestion, index) => {
            const li = document.createElement('li');
            li.className = 'stagger-item';
            li.style.animationDelay = `${index * 0.1}s`;
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'Your post looks good! Keep creating valuable content.';
        suggestionsList.appendChild(li);
    }
    
    // Show results section with animation
    resultsSection.style.display = 'block';
    resultsSection.classList.add('reveal');
    
    // Scroll to results smoothly
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
    
    // Reset feedback form
    resetFeedbackForm();
}

// Show Error Message
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    
    // Scroll to error
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Feedback Form Handling
const feedbackButtons = document.querySelectorAll('.btn-feedback');
let selectedFeedback = null;

feedbackButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove selected class from all buttons
        feedbackButtons.forEach(btn => btn.classList.remove('selected'));
        
        // Add selected class to clicked button
        button.classList.add('selected');
        selectedFeedback = button.dataset.helpful;
        
        // Show comment section and submit button
        document.getElementById('commentSection').style.display = 'block';
        document.getElementById('submitFeedbackBtn').style.display = 'block';
    });
});

// Feedback Form Submission
const feedbackForm = document.getElementById('feedbackForm');
if (feedbackForm) {
    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!selectedFeedback) {
            return;
        }
        
        const comment = document.getElementById('feedbackComment').value.trim();
        const postText = document.getElementById('postText').value.trim();
        
        try {
            const response = await fetch(`${API_BASE_URL}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: getUserId(),
                    post_text: postText,
                    helpful: selectedFeedback === 'yes',
                    comment: comment
                })
            });

            if (response.ok) {
                // Show success message
                document.getElementById('feedbackForm').style.display = 'none';
                document.getElementById('feedbackSuccess').style.display = 'block';
            }
            
        } catch (error) {
            console.error('Error submitting feedback:', error);
            // Still show success to user even if backend fails
            document.getElementById('feedbackForm').style.display = 'none';
            document.getElementById('feedbackSuccess').style.display = 'block';
        }
    });
}

// Reset Feedback Form
function resetFeedbackForm() {
    selectedFeedback = null;
    feedbackButtons.forEach(btn => btn.classList.remove('selected'));
    document.getElementById('commentSection').style.display = 'none';
    document.getElementById('submitFeedbackBtn').style.display = 'none';
    document.getElementById('feedbackComment').value = '';
    document.getElementById('feedbackForm').style.display = 'block';
    document.getElementById('feedbackSuccess').style.display = 'none';
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
