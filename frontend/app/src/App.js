import './App.css';
import Flashcard from './components/Flashcard.js';

const lessonSummary = {
  lessonId: 1,
  summary: 'Welcome to today\'s financial lesson! We\'re delving into several core concepts that are pivotal in the world of finance and investment analysis. Our focus will be on ethical considerations in financial reporting, inventory accounting under different standards, valuation of stocks and bonds, and option pricing models. Let\'s break these down:\n' +
    '\n' +
    'Ethical Considerations in Financial Reporting\n' +
    '\n' +
    'Ethical practices in financial analysis are paramount. A key principle here is the fair and equitable treatment of all clients. When analysts share draft reports, even with well-intentioned goals, it can create conflicts of interest and issues of confidentiality. Analysts must avoid practices that could disadvantage some clients over others. This falls under the larger umbrella of ethical conduct in finance, which includes transparency, fairness, and integrity.\n' +
    '\n' +
    'Inventory Accounting: IFRS vs. US GAAP\n' +
    '\n' +
    'In inventory accounting, the International Financial Reporting Standards (IFRS) and U.S. Generally Accepted Accounting Principles (GAAP) differ. Key to understanding these differences is the concept of inventory valuation. Under IFRS, inventory is carried at the lower of cost or net realizable value, whereas GAAP uses the lower of cost or market value. These differing standards can significantly impact reported assets and cost of goods sold, influencing a company\'s financial health appearance.\n' +
    '\n' +
    'Stock Valuation: Justified Forward P/E\n' +
    '\n' +
    'The Price-to-Earnings (P/E) ratio is a fundamental concept in stock valuation. In assessing a stock\'s value, analysts often look at earnings growth, payout ratios, and required rates of return. The justified forward P/E ratio, which incorporates these factors, helps determine a stock\'s fair value based on its future earnings potential. This approach involves understanding historical performance and projecting future earnings, considering factors like dividends and overall company profitability.\n' +
    '\n' +
    'Bond Portfolio Duration\n' +
    '\n' +
    'Duration is a critical concept in bond investment, measuring a bond\'s price sensitivity to interest rate changes. It reflects the weighted average time until a bond\'s cash flows are received. In a portfolio context, the duration of each bond contributes to the overall portfolio duration, which is a measure of the portfolio\'s interest rate risk. Portfolio duration is a strategic tool for managing risk and aligning investment goals with market expectations.\n' +
    '\n' +
    'Option Pricing: Binomial Model\n' +
    '\n' +
    'In option pricing, the binomial model is a versatile and intuitive tool. It evaluates options by simulating different paths an underlying asset’s price could take. A key factor here is the probability of price movements (upward or downward). An increase in the probability of the asset\'s price rising typically leads to a higher valuation of call options. This concept underlies much of options trading and risk management strategies.\n' +
    '\n'
}

const flashcards = [
  {
    id: 1,
    question: "Sumita Khatri wrote a research report and followed the necessary due diligence steps before sharing the report with her client. It turned out that there was a mistake in the report. This was pointed out by her client. Khatri apologized and re-submitted the corrected report. Did Khatri violate any CFA Institute Standards?",
    answers: ['No.', 'Yes, relating to performance presentation.', 'Yes, relating to misconduct.'],
    correctAnswer: 0,
    lessonFinished: false
  },
  {
    id: 17,
    question: 'Aryana Reid, CFA, is a private wealth manager. She writes a popular blog called “Aryana’s Investments” that has several thousand subscribers. The objective of the blog is to attract new clients; every post is also sent as an e-mail to its subscribers. The blog posts are usually a detailed analysis about her investment recommendations and actions. Recently, Reid issued a sell recommendation for Jubilant Inc. However, a few days after publishing her initial recommendation, she decides to change the recommendation from sell to buy based on some new information. In order to comply with the CFA Institute Standards, which of the following is the most appropriate method for disseminating the change in investment recommendation?',
    answers: ['Publish the post and send it as a mail to the blog subscribers.',
      'Publish the post, send a mail to blog subscribers and email her clients simultaneously.',
      'Email her clients first.'],
    correctAnswer: 0,
    lessonFinished: false
  },
  {
    id: 42,
    question: 'Justin Zoghlin, CFA, was hired as a wealth manager to manage the $2 billion estate of a family in Oklahoma a year ago. He was given the flexibility to choose his working hours. When Zoghlin took the job, he served as the President of his religious community that conducted social welfare programs on a regular basis. In addition, he managed the investments for his large extended family. He did not get paid for his religious community activity or the family investments. Seeing the impressive returns he generated, his friends persuaded him to manage their investments, as well. Now, a year later, he has stopped serving the religious community. He manages investments for non-family members, but charges 10% of the portfolio value as his fee. Zoghlin has not informed his employer of any of these activities. With regard to which of the business activities, has Zoghlin least likely violated the CFA Institute Standards of Professional Conduct?',
    answers: ['Serving the religious community.', 'Managing non-family investments.', 'Managing family investments.'],
    correctAnswer: 0,
    lessonFinished: true
  }
];

function App() {
  return (
    <div className="App">
      <Flashcard lessonSummary={lessonSummary} flashcards={flashcards}></Flashcard>
    </div>
  );
}

export default App;
