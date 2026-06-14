function y = exponential_smooth(values, alpha, initial)
%EXPONENTIAL_SMOOTH Reference MATLAB implementation for parity testing.
%
% y(1) = values(1) when initial is omitted, otherwise initial.
% y(i) = alpha * values(i) + (1 - alpha) * y(i - 1).

    if nargin < 3
        initial = values(1);
    end

    if alpha < 0 || alpha > 1
        error("exponential_smooth:InvalidAlpha", "alpha must be between 0 and 1");
    end

    values = double(values(:));
    if isempty(values)
        error("exponential_smooth:EmptyInput", "values must contain at least one sample");
    end

    y = zeros(size(values));
    y(1) = double(initial);
    for index = 2:numel(values)
        y(index) = alpha * values(index) + (1 - alpha) * y(index - 1);
    end
end
