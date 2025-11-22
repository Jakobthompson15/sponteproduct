export interface KeywordRanking {
  pos: string;
  keyword: string;
}

export interface Industry {
  name: string;
  keywords: KeywordRanking[];
}

export const industries: Industry[] = [
  // Food & Beverage
  {
    name: "Pizza Restaurant",
    keywords: [
      { pos: "#1", keyword: "best pizza near me" },
      { pos: "#2", keyword: "pizza delivery" },
      { pos: "#1", keyword: "italian restaurant" },
      { pos: "#3", keyword: "family restaurant" }
    ]
  },
  {
    name: "Coffee Shop",
    keywords: [
      { pos: "#1", keyword: "coffee shop near me" },
      { pos: "#2", keyword: "best espresso" },
      { pos: "#1", keyword: "wifi coffee shop" },
      { pos: "#3", keyword: "breakfast cafe" }
    ]
  },
  {
    name: "Chinese Restaurant",
    keywords: [
      { pos: "#1", keyword: "chinese food delivery" },
      { pos: "#2", keyword: "dim sum near me" },
      { pos: "#1", keyword: "chinese takeout" },
      { pos: "#3", keyword: "best asian food" }
    ]
  },
  {
    name: "Mexican Restaurant",
    keywords: [
      { pos: "#1", keyword: "tacos near me" },
      { pos: "#2", keyword: "mexican restaurant" },
      { pos: "#1", keyword: "margaritas and tacos" },
      { pos: "#3", keyword: "authentic mexican" }
    ]
  },
  {
    name: "Bakery",
    keywords: [
      { pos: "#1", keyword: "fresh bread near me" },
      { pos: "#2", keyword: "custom cakes" },
      { pos: "#1", keyword: "bakery open now" },
      { pos: "#3", keyword: "artisan bakery" }
    ]
  },
  {
    name: "Craft Brewery",
    keywords: [
      { pos: "#1", keyword: "craft beer near me" },
      { pos: "#2", keyword: "brewpub" },
      { pos: "#1", keyword: "happy hour specials" },
      { pos: "#3", keyword: "best local brewery" }
    ]
  },
  {
    name: "Sushi Restaurant",
    keywords: [
      { pos: "#1", keyword: "sushi near me" },
      { pos: "#2", keyword: "all you can eat sushi" },
      { pos: "#1", keyword: "fresh sushi" },
      { pos: "#3", keyword: "japanese restaurant" }
    ]
  },
  {
    name: "Ice Cream Shop",
    keywords: [
      { pos: "#1", keyword: "ice cream near me" },
      { pos: "#2", keyword: "gelato shop" },
      { pos: "#1", keyword: "best ice cream" },
      { pos: "#3", keyword: "dessert near me" }
    ]
  },

  // Home Services
  {
    name: "HVAC Services",
    keywords: [
      { pos: "#1", keyword: "ac repair near me" },
      { pos: "#2", keyword: "hvac installation" },
      { pos: "#1", keyword: "emergency hvac" },
      { pos: "#3", keyword: "furnace repair" }
    ]
  },
  {
    name: "Plumbing Services",
    keywords: [
      { pos: "#1", keyword: "emergency plumber" },
      { pos: "#2", keyword: "plumber near me" },
      { pos: "#1", keyword: "pipe repair" },
      { pos: "#3", keyword: "water heater install" }
    ]
  },
  {
    name: "Electrical Services",
    keywords: [
      { pos: "#1", keyword: "electrician near me" },
      { pos: "#2", keyword: "electrical repair" },
      { pos: "#1", keyword: "panel upgrade" },
      { pos: "#3", keyword: "emergency electrician" }
    ]
  },
  {
    name: "Landscaping",
    keywords: [
      { pos: "#1", keyword: "landscaping services" },
      { pos: "#2", keyword: "lawn care near me" },
      { pos: "#1", keyword: "landscape design" },
      { pos: "#3", keyword: "tree trimming" }
    ]
  },
  {
    name: "Roofing Contractor",
    keywords: [
      { pos: "#1", keyword: "roof repair near me" },
      { pos: "#2", keyword: "roofing contractor" },
      { pos: "#1", keyword: "roof replacement" },
      { pos: "#3", keyword: "emergency roof repair" }
    ]
  },
  {
    name: "House Cleaning",
    keywords: [
      { pos: "#1", keyword: "cleaning service near me" },
      { pos: "#2", keyword: "maid service" },
      { pos: "#1", keyword: "deep cleaning" },
      { pos: "#3", keyword: "move out cleaning" }
    ]
  },
  {
    name: "Pest Control",
    keywords: [
      { pos: "#1", keyword: "pest control near me" },
      { pos: "#2", keyword: "termite inspection" },
      { pos: "#1", keyword: "bed bug treatment" },
      { pos: "#3", keyword: "exterminator" }
    ]
  },
  {
    name: "Painting Contractor",
    keywords: [
      { pos: "#1", keyword: "house painter near me" },
      { pos: "#2", keyword: "interior painting" },
      { pos: "#1", keyword: "exterior painting" },
      { pos: "#3", keyword: "painting contractor" }
    ]
  },
  {
    name: "Locksmith",
    keywords: [
      { pos: "#1", keyword: "locksmith near me" },
      { pos: "#2", keyword: "emergency locksmith" },
      { pos: "#1", keyword: "car lockout service" },
      { pos: "#3", keyword: "lock replacement" }
    ]
  },
  {
    name: "Handyman Services",
    keywords: [
      { pos: "#1", keyword: "handyman near me" },
      { pos: "#2", keyword: "home repair" },
      { pos: "#1", keyword: "handyman services" },
      { pos: "#3", keyword: "odd jobs" }
    ]
  },

  // Health & Wellness
  {
    name: "Dental Practice",
    keywords: [
      { pos: "#1", keyword: "dentist near me" },
      { pos: "#2", keyword: "teeth cleaning" },
      { pos: "#1", keyword: "emergency dentist" },
      { pos: "#3", keyword: "family dentistry" }
    ]
  },
  {
    name: "Chiropractor",
    keywords: [
      { pos: "#1", keyword: "chiropractor near me" },
      { pos: "#2", keyword: "back pain relief" },
      { pos: "#1", keyword: "spinal adjustment" },
      { pos: "#3", keyword: "sports chiropractor" }
    ]
  },
  {
    name: "Physical Therapy",
    keywords: [
      { pos: "#1", keyword: "physical therapy near me" },
      { pos: "#2", keyword: "sports rehab" },
      { pos: "#1", keyword: "injury recovery" },
      { pos: "#3", keyword: "pt clinic" }
    ]
  },
  {
    name: "Veterinary Clinic",
    keywords: [
      { pos: "#1", keyword: "vet near me" },
      { pos: "#2", keyword: "emergency vet" },
      { pos: "#1", keyword: "dog vaccinations" },
      { pos: "#3", keyword: "animal hospital" }
    ]
  },
  {
    name: "Urgent Care",
    keywords: [
      { pos: "#1", keyword: "urgent care near me" },
      { pos: "#2", keyword: "walk in clinic" },
      { pos: "#1", keyword: "emergency care" },
      { pos: "#3", keyword: "open now" }
    ]
  },
  {
    name: "Massage Therapy",
    keywords: [
      { pos: "#1", keyword: "massage near me" },
      { pos: "#2", keyword: "deep tissue massage" },
      { pos: "#1", keyword: "therapeutic massage" },
      { pos: "#3", keyword: "spa massage" }
    ]
  },
  {
    name: "Medical Spa",
    keywords: [
      { pos: "#1", keyword: "botox near me" },
      { pos: "#2", keyword: "laser hair removal" },
      { pos: "#1", keyword: "med spa" },
      { pos: "#3", keyword: "skin rejuvenation" }
    ]
  },
  {
    name: "Optometry",
    keywords: [
      { pos: "#1", keyword: "eye doctor near me" },
      { pos: "#2", keyword: "eye exam" },
      { pos: "#1", keyword: "glasses near me" },
      { pos: "#3", keyword: "contact lenses" }
    ]
  },

  // Professional Services
  {
    name: "Personal Injury Law",
    keywords: [
      { pos: "#1", keyword: "personal injury lawyer" },
      { pos: "#2", keyword: "car accident attorney" },
      { pos: "#1", keyword: "slip and fall lawyer" },
      { pos: "#3", keyword: "injury claim" }
    ]
  },
  {
    name: "Family Law",
    keywords: [
      { pos: "#1", keyword: "divorce attorney near me" },
      { pos: "#2", keyword: "family law lawyer" },
      { pos: "#1", keyword: "child custody lawyer" },
      { pos: "#3", keyword: "divorce mediation" }
    ]
  },
  {
    name: "Accounting Firm",
    keywords: [
      { pos: "#1", keyword: "tax accountant near me" },
      { pos: "#2", keyword: "cpa services" },
      { pos: "#1", keyword: "tax preparation" },
      { pos: "#3", keyword: "business accounting" }
    ]
  },
  {
    name: "Real Estate Agent",
    keywords: [
      { pos: "#1", keyword: "realtor near me" },
      { pos: "#2", keyword: "homes for sale" },
      { pos: "#1", keyword: "real estate agent" },
      { pos: "#3", keyword: "buy house" }
    ]
  },
  {
    name: "Insurance Agency",
    keywords: [
      { pos: "#1", keyword: "insurance agent near me" },
      { pos: "#2", keyword: "auto insurance" },
      { pos: "#1", keyword: "home insurance quote" },
      { pos: "#3", keyword: "business insurance" }
    ]
  },
  {
    name: "Financial Advisor",
    keywords: [
      { pos: "#1", keyword: "financial advisor near me" },
      { pos: "#2", keyword: "retirement planning" },
      { pos: "#1", keyword: "wealth management" },
      { pos: "#3", keyword: "investment advisor" }
    ]
  },

  // Personal Care
  {
    name: "Hair Salon",
    keywords: [
      { pos: "#1", keyword: "hair salon near me" },
      { pos: "#2", keyword: "women's haircut" },
      { pos: "#1", keyword: "balayage near me" },
      { pos: "#3", keyword: "best hairstylist" }
    ]
  },
  {
    name: "Barber Shop",
    keywords: [
      { pos: "#1", keyword: "barber near me" },
      { pos: "#2", keyword: "men's haircut" },
      { pos: "#1", keyword: "beard trim" },
      { pos: "#3", keyword: "traditional barber" }
    ]
  },
  {
    name: "Nail Salon",
    keywords: [
      { pos: "#1", keyword: "nail salon near me" },
      { pos: "#2", keyword: "manicure pedicure" },
      { pos: "#1", keyword: "gel nails" },
      { pos: "#3", keyword: "nail art" }
    ]
  },
  {
    name: "Day Spa",
    keywords: [
      { pos: "#1", keyword: "spa near me" },
      { pos: "#2", keyword: "facial treatments" },
      { pos: "#1", keyword: "couples massage" },
      { pos: "#3", keyword: "spa packages" }
    ]
  },
  {
    name: "Fitness Center",
    keywords: [
      { pos: "#1", keyword: "gym near me" },
      { pos: "#2", keyword: "personal training" },
      { pos: "#1", keyword: "fitness classes" },
      { pos: "#3", keyword: "24 hour gym" }
    ]
  },

  // Automotive
  {
    name: "Auto Repair",
    keywords: [
      { pos: "#1", keyword: "auto repair near me" },
      { pos: "#2", keyword: "mechanic" },
      { pos: "#1", keyword: "car repair" },
      { pos: "#3", keyword: "brake service" }
    ]
  },
  {
    name: "Car Wash",
    keywords: [
      { pos: "#1", keyword: "car wash near me" },
      { pos: "#2", keyword: "auto detailing" },
      { pos: "#1", keyword: "hand car wash" },
      { pos: "#3", keyword: "full service car wash" }
    ]
  },
  {
    name: "Tire Shop",
    keywords: [
      { pos: "#1", keyword: "tire shop near me" },
      { pos: "#2", keyword: "tire installation" },
      { pos: "#1", keyword: "wheel alignment" },
      { pos: "#3", keyword: "tire repair" }
    ]
  },
  {
    name: "Auto Detailing",
    keywords: [
      { pos: "#1", keyword: "auto detailing near me" },
      { pos: "#2", keyword: "ceramic coating" },
      { pos: "#1", keyword: "interior detailing" },
      { pos: "#3", keyword: "paint correction" }
    ]
  },

  // Retail & Other
  {
    name: "Florist",
    keywords: [
      { pos: "#1", keyword: "florist near me" },
      { pos: "#2", keyword: "flower delivery" },
      { pos: "#1", keyword: "wedding flowers" },
      { pos: "#3", keyword: "same day flowers" }
    ]
  },
  {
    name: "Pet Store",
    keywords: [
      { pos: "#1", keyword: "pet store near me" },
      { pos: "#2", keyword: "dog grooming" },
      { pos: "#1", keyword: "pet supplies" },
      { pos: "#3", keyword: "aquarium shop" }
    ]
  },
  {
    name: "Photography Studio",
    keywords: [
      { pos: "#1", keyword: "photographer near me" },
      { pos: "#2", keyword: "family photos" },
      { pos: "#1", keyword: "wedding photographer" },
      { pos: "#3", keyword: "headshot photographer" }
    ]
  },
  {
    name: "Storage Facility",
    keywords: [
      { pos: "#1", keyword: "storage units near me" },
      { pos: "#2", keyword: "self storage" },
      { pos: "#1", keyword: "climate controlled" },
      { pos: "#3", keyword: "rv storage" }
    ]
  }
];
