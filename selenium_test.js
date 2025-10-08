#!/usr/bin/env node
/**
 * Node.js Selenium test script to access localhost:3000 from Docker container
 */

const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const fs = require('fs');

async function createChromeOptions() {
    const options = new chrome.Options();
    options.addArguments('--no-sandbox');
    options.addArguments('--disable-dev-shm-usage');
    options.addArguments('--disable-gpu');
    options.addArguments('--window-size=1920,1080');
    options.addArguments('--disable-extensions');
    options.addArguments('--disable-plugins');
    options.addArguments('--disable-images');
    return options;
}

async function testLocalhostAccess() {
    console.log('🚀 Starting Selenium test...');
    
    const webdriverUrl = 'http://localhost:4444/wd/hub';
    const targetUrl = 'http://host.docker.internal:3000';
    
    let driver;
    
    try {
        // Create Chrome options
        const chromeOptions = await createChromeOptions();
        
        // Connect to remote WebDriver
        console.log(`Connecting to WebDriver at ${webdriverUrl}...`);
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(chromeOptions)
            .usingServer(webdriverUrl)
            .build();
        
        console.log(`Navigating to ${targetUrl}...`);
        await driver.get(targetUrl);
        
        // Wait for page to load
        await driver.wait(until.titleIs(await driver.getTitle()), 10000);
        
        // Get page title
        const title = await driver.getTitle();
        console.log('✅ Page loaded successfully!');
        console.log(`Page title: ${title}`);
        
        // Take a screenshot
        const screenshot = await driver.takeScreenshot();
        const screenshotPath = '/tmp/selenium_test_screenshot.png';
        fs.writeFileSync(screenshotPath, screenshot, 'base64');
        console.log(`Screenshot saved to: ${screenshotPath}`);
        
        // Try to find some common elements
        try {
            const body = await driver.findElement(By.tagName('body'));
            const bodyText = await body.getText();
            console.log(`Body content length: ${bodyText.length} characters`);
        } catch (error) {
            console.log(`Could not find body element: ${error.message}`);
        }
        
        console.log('✅ Test completed successfully!');
        return true;
        
    } catch (error) {
        console.log(`❌ Test failed: ${error.message}`);
        return false;
        
    } finally {
        if (driver) {
            await driver.quit();
            console.log('WebDriver session closed');
        }
    }
}

async function checkWebDriverStatus() {
    try {
        const response = await fetch('http://localhost:4444/wd/hub/status');
        if (response.ok) {
            console.log('✅ WebDriver is running and accessible');
            return true;
        } else {
            console.log('❌ WebDriver is not responding properly');
            return false;
        }
    } catch (error) {
        console.log(`❌ Cannot connect to WebDriver: ${error.message}`);
        console.log('Make sure Docker container is running: docker-compose up -d');
        return false;
    }
}

async function main() {
    console.log('🔍 Selenium Test: Accessing localhost:3000 from Docker container');
    console.log('='.repeat(70));
    
    // Check if WebDriver is accessible
    const webdriverOk = await checkWebDriverStatus();
    if (!webdriverOk) {
        process.exit(1);
    }
    
    // Run the test
    const success = await testLocalhostAccess();
    
    if (success) {
        console.log('\n🎉 SUCCESS! Your setup is working correctly!');
        console.log('You can now run Selenium tests against your localhost:3000 service.');
    } else {
        console.log('\n💡 Troubleshooting:');
        console.log('1. Ensure your dev server is running on localhost:3000');
        console.log('2. Check Docker container: docker-compose ps');
        console.log('3. View container logs: docker-compose logs selenium-chrome');
        console.log('4. Access noVNC desktop: http://localhost:7900');
        process.exit(1);
    }
}

// Run the main function
main().catch(console.error);
