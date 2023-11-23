spec = [
    {
        method: 'GET',
        endpoint: '/lessonSummary',
        params: {
            lessonId: 1
        },
        response: {
            summary: 'Lorem ipsum dolor sit amet...'
        }
    },

    {
        method: 'GET',
        endpoint: '/question',
        params: {
            lessonId: 1,
            questionNumber: 1
        },
        response: {
            id: '17',
            question: 'Which of the following is not a requirement of GIPS for composite construction?',
            answers: [
                'one or more portfolios.',
                'portfolios selected on an ex-post basis.',
                'portfolios managed according to a similar investment strategy.'
            ],
            correctAnswer: 0, // the position in the array which is the correct answer
            lessonFinished: true // this should be true if it is the last question
        }
    },


    {
        method: 'POST',
        endpoint: '/question',
        data: {
            id: '17', // question id
            answer: 1,  // their answer
            timeTaken: 23  // in seconds
        }
    },
    
    {
        method: 'GET',
        endpoint: '/explain',
        params: {
            questionId: 17
        },
        response: {
            explanation: 'Lorem ipsum dolor...'
        }
    },
    
    {
        method: 'GET',
        endpoint: '/visualise',
        response: [
            {x:5, y:10, zScore: 0.4, category: 'Quantitave finance'},
            {x:5, y:10, zScore: 0.4, category: 'Quantitave finance'},
        ]
    }
]