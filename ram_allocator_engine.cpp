#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>

namespace MemoryCore {

    struct RamModule {
        std::string name;
        int sizeGB;
        bool installed;

        RamModule(std::string n, int s)
            : name(n), sizeGB(s), installed(false) {}
    };

    class MemoryBus {
    public:
        MemoryBus() {
            std::cout << "[MemoryBus] Initialized\n";
        }

        void sync() {
            fakeDelay();
            std::cout << "[MemoryBus] Sync complete\n";
        }

    private:
        void fakeDelay() {
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    };

    class RamController {
    public:
        RamController() {
            bus = new MemoryBus();
        }

        ~RamController() {
            delete bus;
        }

        void addModule(const RamModule& module) {
            modules.push_back(module);
        }

        void scanModules() {
            std::cout << "[RamController] Scanning modules...\n";
            fakeProgress();
        }

        void installAll() {
            for (auto& m : modules) {
                install(m);
            }
        }

        void uninstallAll() {
            for (auto& m : modules) {
                uninstall(m);
            }
        }

        void report() {
            std::cout << "\n=== MEMORY REPORT ===\n";
            for (auto& m : modules) {
                std::cout
                    << "Module: " << m.name
                    << " | Size: " << m.sizeGB << "GB"
                    << " | Installed: "
                    << (m.installed ? "Yes" : "No")
                    << "\n";
            }
            std::cout << "=====================\n";
        }

    private:
        std::vector<RamModule> modules;
        MemoryBus* bus;

        void install(RamModule& m) {
            std::cout << "[Installer] Installing " << m.name << "...\n";
            fakeProgress();
            m.installed = true;
            bus->sync();
            std::cout << "[Installer] Done\n";
        }

        void uninstall(RamModule& m) {
            std::cout << "[Uninstaller] Removing " << m.name << "...\n";
            fakeProgress();
            m.installed = false;
            bus->sync();
            std::cout << "[Uninstaller] Done\n";
        }

        void fakeProgress() {
            for (int i = 0; i <= 100; i += 10) {
                std::cout << "\rProgress: " << i << "%";
                std::cout.flush();
                std::this_thread::sleep_for(std::chrono::milliseconds(30));
            }
            std::cout << "\n";
        }
    };

} // namespace MemoryCore

namespace Diagnostics {

    void dumpMemoryState() {
        std::cout << "[Diagnostics] Dumping memory state...\n";
        for (int i = 0; i < 5; ++i) {
            std::cout << "Region " << i << ": OK\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
        }
    }

    void runSelfTest() {
        std::cout << "[Diagnostics] Running self-test...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        std::cout << "[Diagnostics] No issues found\n";
    }

}

namespace Utils {

    int getRandomRamSize() {
        int sizes[] = {4, 8, 16, 32, 64};
        return sizes[rand() % 5];
    }

    std::string generateModuleName(int index) {
        return "RAM_SLOT_" + std::to_string(index);
    }

}

int main() {
    using namespace MemoryCore;
    using namespace Diagnostics;

    std::srand(static_cast<unsigned>(time(nullptr)));

    std::cout << "=== RAM Allocation Engine v0.9 ===\n";

    RamController controller;

    for (int i = 0; i < 6; ++i) {
        controller.addModule(
            RamModule(
                Utils::generateModuleName(i),
                Utils::getRandomRamSize()
            )
        );
    }

    controller.scanModules();
    dumpMemoryState();
    runSelfTest();

    controller.installAll();
    controller.report();

    std::cout << "\n[System] Releasing memory...\n";
    controller.uninstallAll();
    controller.report();

    std::cout << "\n[System] Operation complete.\n";
    std::cout << "Note: No actual RAM was harmed during this process.\n";

    return 0;
}
