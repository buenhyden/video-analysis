
const Footer = () =>
{
    return (
        <footer className="border-t border-slate-800 bg-slate-950 py-12 mt-12">
            <div className="max-w-7xl mx-auto px-4 text-center">
                <p className="text-slate-500 mb-4">© 2024 Visual Portfolio. All rights reserved.</p>
                <div className="flex justify-center gap-6 text-slate-600">
                    <a href="#" className="hover:text-indigo-400 transition-colors">Instagram</a>
                    <a href="#" className="hover:text-indigo-400 transition-colors">Vimeo</a>
                    <a href="#" className="hover:text-indigo-400 transition-colors">LinkedIn</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;