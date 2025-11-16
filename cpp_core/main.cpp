#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// ========== 1. ABSTRACTION & INHERITANCE ==========
// Abstract Base Class (Abstraction)
class Indicator
{
protected:
    std::vector<double> prices;
    int period;

public:
    // Constructor
    Indicator(const std::vector<double> &data, int p) : prices(data), period(p) {}

    // Pure virtual function (Abstraction)
    virtual double calculate() = 0;

    // Virtual destructor
    virtual ~Indicator() {}
};

// ========== 2. INHERITANCE & POLYMORPHISM ==========
// Derived Class (Inheritance)
class SMA : public Indicator
{
public:
    // Constructor
    SMA(const std::vector<double> &data, int p) : Indicator(data, p) {}

    // Override virtual function (Polymorphism)
    double calculate() override
    {
        if (prices.size() < static_cast<size_t>(period))
            return 0.0;

        double sum = 0.0;
        for (size_t i = prices.size() - period; i < prices.size(); ++i)
        {
            sum += prices[i];
        }
        return sum / period;
    }
};

// ========== 3. ENCAPSULATION ==========
// Class with private data and public methods
class StockAnalyzer
{
private:
    // Private data members (Encapsulation)
    std::vector<double> closePrices;
    int analysisPeriod;
    double result;

public:
    // Constructor
    StockAnalyzer(const std::vector<double> &prices, int period)
        : closePrices(prices), analysisPeriod(period), result(0.0) {}

    // Public method to perform analysis
    void analyze()
    {
        // Create indicator object (Polymorphism in action)
        Indicator *indicator = new SMA(closePrices, analysisPeriod);
        result = indicator->calculate();
        delete indicator;
    }

    // Getter method (Encapsulation)
    double getResult() const
    {
        return result;
    }

    int getPeriod() const
    {
        return analysisPeriod;
    }
};

int main()
{
    // Read JSON input
    std::stringstream buffer;
    buffer << std::cin.rdbuf();
    json input = json::parse(buffer.str());

    std::vector<double> closePrices = input["close_prices"].get<std::vector<double>>();
    int period = input.value("period", 5);

    // Create analyzer object
    StockAnalyzer analyzer(closePrices, period);

    // Perform analysis
    analyzer.analyze();

    // Generate output
    json output;
    std::string key = std::to_string(period) + "_day_SMA";
    output[key] = analyzer.getResult();

    // Backward compatibility
    if (period == 5)
    {
        output["5_day_SMA"] = analyzer.getResult();
    }

    std::cout << output.dump() << std::endl;

    return 0;
}