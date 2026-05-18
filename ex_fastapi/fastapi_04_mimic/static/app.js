const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultBody = document.getElementById('result-body');
const resultCount = document.getElementById('result-count');
const loadingIndicator = document.getElementById('loading');
const resultContainer = document.getElementById('result-container');
const errorMessageDiv = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (!query) return;

    // View 상태 설정
    showLoading();

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

        if (response.ok) {
            const data = await response.json();
            renderResults(data);
        } else {
            const errData = await response.json();
            showError(`Error: ${errData.detail || '검색 과정에서 오류가 발생했습니다.'}`);
        }
    } catch (error) {
        console.error("Search Error:", error);
        showError("서버와 통신할 수 없습니다. FastAPI 서버(`uvicorn main:app --reload`)가 실행 중인지 확인해주세요.");
    }
});

function showLoading() {
    loadingIndicator.classList.remove('hidden');
    resultContainer.classList.add('hidden');
    errorMessageDiv.classList.add('hidden');
    resultCount.innerText = '검색 중...';
}

function showError(message) {
    loadingIndicator.classList.add('hidden');
    resultContainer.classList.add('hidden');
    errorMessageDiv.classList.remove('hidden');
    errorText.innerText = message;
    resultCount.innerText = '오류';
}

function renderResults(results) {
    loadingIndicator.classList.add('hidden');
    resultContainer.classList.remove('hidden');
    errorMessageDiv.classList.add('hidden');

    resultCount.innerText = `${results.length} 건`;
    resultBody.innerHTML = '';

    if (results.length === 0) {
        resultBody.innerHTML = `
            <tr>
                <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                    <i class="fas fa-folder-open text-3xl mb-3 text-gray-300"></i>
                    <p>검색 결과가 없습니다. 다른 키워드로 시도해 보세요.</p>
                </td>
            </tr>
        `;
        return;
    }

    results.forEach(item => {
        // 타입에 따른 뱃지 색상 지정
        const badgeColor = item.code_type.includes('ICD') ? 'bg-purple-100 text-purple-800' : 'bg-teal-100 text-teal-800';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50 transition duration-150';

        tr.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${badgeColor}">
                    ${item.code_type}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 border-r border-gray-100">
                ${item.code}
            </td>
            <td class="px-6 py-4 text-sm text-gray-700 leading-relaxed border-r border-gray-100">
                ${item.english_name}
            </td>
            <td class="px-6 py-4 text-sm font-medium text-blue-800 leading-relaxed bg-blue-50/50 border-l-2 border-blue-100">
                ${item.korean_name}
            </td>
        `;

        resultBody.appendChild(tr);
    });
}
