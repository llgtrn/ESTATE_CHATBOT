import { http, HttpResponse } from 'msw';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const handlers = [
  // Session endpoints
  http.post(`${API_BASE_URL}/sessions`, () => {
    return HttpResponse.json({
      session_id: 'mock-session-123',
      status: 'active',
      language: 'ja',
      created_at: new Date().toISOString(),
    });
  }),

  http.get(`${API_BASE_URL}/sessions/:sessionId`, ({ params }) => {
    return HttpResponse.json({
      session_id: params.sessionId,
      status: 'active',
      language: 'ja',
      turn_count: 5,
      token_count: 1500,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }),

  http.delete(`${API_BASE_URL}/sessions/:sessionId`, () => {
    return new HttpResponse(null, { status: 204 });
  }),

  // Message endpoints
  http.post(`${API_BASE_URL}/sessions/:sessionId/messages`, async ({ request }) => {
    const body = (await request.json()) as { message: string; language?: string };

    return HttpResponse.json({
      message_id: 'mock-msg-123',
      session_id: 'mock-session-123',
      response: `こんにちは！「${body.message}」について詳しく教えてください。`,
      intent: 'greeting',
      confidence: 0.95,
      entities: {},
      language: body.language || 'ja',
    });
  }),

  http.get(`${API_BASE_URL}/sessions/:sessionId/messages`, () => {
    return HttpResponse.json({
      session_id: 'mock-session-123',
      messages: [
        {
          message_id: 'msg-1',
          session_id: 'mock-session-123',
          role: 'user',
          content: 'こんにちは',
          language: 'ja',
          created_at: new Date().toISOString(),
        },
        {
          message_id: 'msg-2',
          session_id: 'mock-session-123',
          role: 'assistant',
          content: 'こんにちは！お探しの物件について教えてください。',
          language: 'ja',
          created_at: new Date().toISOString(),
        },
      ],
      total: 2,
    });
  }),

  // Brief endpoints
  http.get(`${API_BASE_URL}/briefs/:briefId`, ({ params }) => {
    return HttpResponse.json({
      brief_id: params.briefId,
      session_id: 'mock-session-123',
      property_type: 'buy',
      status: 'draft',
      location: '東京都渋谷区',
      budget_min: 50000000,
      budget_max: 80000000,
      rooms: '3LDK',
      data: {},
      completeness_score: 75,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }),

  http.patch(`${API_BASE_URL}/briefs/:briefId`, async ({ params, request }) => {
    const body = await request.json();
    return HttpResponse.json({
      brief_id: params.briefId,
      ...body,
      updated_at: new Date().toISOString(),
    });
  }),

  http.post(`${API_BASE_URL}/briefs/:briefId/submit`, ({ params }) => {
    return HttpResponse.json({
      brief_id: params.briefId,
      status: 'submitted',
      submitted_at: new Date().toISOString(),
    });
  }),

  // Glossary endpoints
  http.get(`${API_BASE_URL}/glossary/search`, ({ request }) => {
    const url = new URL(request.url);
    const query = url.searchParams.get('query') || '';
    const language = url.searchParams.get('language') || 'ja';

    return HttpResponse.json({
      query,
      language,
      results: [
        {
          term_id: 'term-1',
          term: '築年数',
          language: 'ja',
          translation: 'Building Age',
          explanation: '建物が建築されてから経過した年数',
          category: 'property_info',
          examples: ['築10年のマンション'],
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ],
      total: 1,
    });
  }),

  http.get(`${API_BASE_URL}/glossary/terms/:termId`, ({ params }) => {
    return HttpResponse.json({
      term_id: params.termId,
      term: '築年数',
      language: 'ja',
      translation: 'Building Age',
      explanation: '建物が建築されてから経過した年数',
      category: 'property_info',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }),
];
